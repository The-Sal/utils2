class SystemException(Exception):
    def __init__(self, *args, **kwargs):
        pass


class InvalidArgument(SystemException):
    def __init__(self, *args, **kwargs):
        pass


class PathsException(SystemException):
    def __init__(self, *args, **kwargs):
        pass
