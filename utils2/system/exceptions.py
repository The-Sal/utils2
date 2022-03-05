class SystemException(Exception):
    def __init__(self, *args, **kwargs):
        pass


class InvalidArgument(SystemException):
    def __init__(self, *args, **kwargs):
        pass


class PathsException(SystemException):
    def __init__(self, *args, **kwargs):
        pass


# Wrappers

def pathsExceptionWrapper(func):
    """For volatile functions"""

    def _wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as exc:
            val = '"{}" Exception occurred inside function "{}" with the message "{}"'.format(
                str(exc.__class__.__name__), func.__name__, exc.args[0])
            raise PathsException(val)

    return _wrapper
