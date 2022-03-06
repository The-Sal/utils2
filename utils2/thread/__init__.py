import threading

def thread(target, args=None, daemon=False):
    if isinstance(args, str):
        args = (args,)

    elif args is None:
        args = ()

    else:
        args = tuple(args)

    proc = threading.Thread(target=target, args=args, daemon=daemon)
    proc.start()
    return proc


def multiple_threads(function_data, daemon=True):
    """
    Functions must be in a list like so [function1, function2, function3]
    :param daemon:
    true by default
    :param function_data:

    List of Dictionary like so
    function_data = [
        {
        'function' : function
        'args' : [arg1, arg2]
        }
    ]

    :return:
    A list of all the started threads
    """
    obj_s = []
    for f in function_data:
        Args = f['args']
        if Args is None:
            Args = []

        Function = f['function']
        obj_s.append(threading.Thread(target=Function, args=Args, daemon=daemon))

    for o in obj_s:
        o.start()

    return obj_s


class ThreadManager:
    def __init__(self):
        self.threads = []

    def add_thread(self, target, args=None, daemon=False):
        if isinstance(args, str):
            args = (args,)

        elif args is None:
            args = ()

        else:
            args = tuple(args)

        thr = threading.Thread(target=target, args=args, daemon=daemon)
        thr.name = target.__name__
        thr.start()


        self.threads.append(thr)


    def add_multiple_threads(self, function_data, daemon=True):
        threads = multiple_threads(function_data, daemon=daemon)
        self.threads.extend(threads)

    def get_threads(self):
        return self.threads

    def get_threads_count(self):
        return len(self.threads)