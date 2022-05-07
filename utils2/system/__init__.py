"""A package to manage system specific functions, such as file paths, executing commands, etc."""
import os
import signal as _signal
from os import path as _path
from subprocess import Popen, PIPE

try:
    from . import paths
    from ._utils import Process
    from .exceptions import InvalidArgument
except (ImportError, ValueError):
    from exceptions import InvalidArgument
    import paths
    from _utils import Process

# Simple Values
homeDirectory = _path.expanduser('~')


def command(cmd, read=False, supress=False, waitUntilFinished=True):
    """Execute a command and return the output, if desired"""

    def _returnCMD(arg):
        """Return the command"""
        if isinstance(arg, str):
            return arg.split(' ')
        elif isinstance(arg, list):
            return arg
        else:
            InvalidArgument("Invalid argument type: {}".format(type(arg)))

    command_argument = _returnCMD(cmd)
    if read:
        proc = Popen(command_argument, stdout=PIPE, stderr=PIPE)
    else:
        if supress:
            devnull = open(_path.devnull, 'w')
            proc = Popen(command_argument, stdout=devnull, stderr=devnull)
        else:
            proc = Popen(command_argument)

    if waitUntilFinished:
        proc.wait()

    returnOutput = []
    if supress:
        returnOutput.append(proc)
    else:
        if read:
            if waitUntilFinished:
                proc.wait()
                returnOutput.append(proc.stdout.read().decode('utf-8'))
            else:
                returnOutput.append(proc)


        else:
            returnOutput.append(proc)

        return tuple(returnOutput)


def ipAddress(interface='en0'):
    """Return the IP address of the specified interface, default is 'en0'"""
    ip = command(['ipconfig', 'getifaddr', interface], read=True)
    try:
        ip = ip[0].removesuffix('\n')
    except AttributeError or Exception:
        if ip[0].endswith('\n'):
            ip = ip[0][:-1]

    return ip


def kill(pid, signal=_signal.SIGTERM):
    """Kill a process with the specified PID"""
    if not isinstance(pid, int):
        pid = int(pid)
    os.kill(pid, signal)


def allProcesses() -> [Process]:
    """Read all processes running on Mac"""
    allProcs = command(['ps', 'aux'], read=True)[0].split('\n')
    allProcs.pop(0)

    procs = []

    for proc in allProcs:
        components = proc.split(' ')
        index = 0
        for component in components:
            if not component != '':
                components.pop(index)

            index += 1

        for component in components:
            if component == '' or component == ' ' or component == '':
                components.remove(component)

            index += 1

        clean_list = list(dict.fromkeys(components))

        try:
            clean_list.remove('')
        except ValueError:
            pass

        if len(clean_list) == 0:
            continue

        owner = clean_list[0]
        pid = clean_list[1]
        cpu_percent = clean_list[2]
        memory_percent = clean_list[3]
        clean_list.pop(0)
        clean_list.pop(1)
        clean_list.pop(2)
        clean_list.pop(3)
        cmd = ' '.join(clean_list)

        procs.append(Process(owner, pid, cpu_percent, memory_percent, cmd))

    return procs


def foregroundApplication() -> str:
    """Return the foreground application"""
    foreground = command(['osascript', '-e',
                          'tell application "System Events" to name of first application process whose frontmost is '
                          'true'],
                         read=True)[0]


    return foreground.split('\n')[0]

