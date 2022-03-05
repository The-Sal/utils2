"""A package to manage system specific functions, such as file paths, executing commands, etc."""
import os
import socket
import signal as _signal
from os import path as _path
from subprocess import Popen, PIPE
from . import paths


try:
    from .exceptions import InvalidArgument
except (ImportError, ValueError):
    from exceptions import InvalidArgument


# Simple Values
homeDirectory = _path.expanduser('~')
hostName = socket.gethostname()
hostAddress = socket.gethostbyname(hostName)

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
        process = Popen(command_argument, stdout=PIPE, stderr=PIPE)
    else:
        if supress:
            devnull = open(_path.devnull, 'w')
            process = Popen(command_argument, stdout=devnull, stderr=devnull)
        else:
            process = Popen(command_argument)

    if waitUntilFinished:
        process.wait()


    returnOutput = []
    if supress:
        returnOutput.append(process)
    else:
        if read:
            if waitUntilFinished:
                process.wait()
                returnOutput.append(process.stdout.read().decode('utf-8'))
            else:
                returnOutput.append(process)


        else:
            returnOutput.append(process)

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



if __name__ == '__main__':
    print(hostAddress)
