class Process:
    def __init__(self, user, pid, cpu_percent, memory_percent, cmd):
        self.user = user
        self.pid = pid
        self.cpu_percent = cpu_percent
        self.memory_percent = memory_percent
        self.cmd = cmd