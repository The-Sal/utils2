import threading


def thread(target, args=None, daemon=False):
    """Starts a thread and returns the thread object"""
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

    :param daemon: true by default
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



class ThreadPool:
    """A class to decorate functions for async execution"""
    def __init__(self, autostart=False):
        """
        :param autostart: Defines if the threads should be started automatically or stored as a Thread object to be
            called later
        """
        self.autostart = autostart
        self._threads = {
            'Generic': []
        }

    def __call__(self, autostart=None, identifier=None):
        """:param autostart: Defines if the threads should be started automatically on an individual function
        :param identifier: Defines the identifier to store the thread under"""
        def outer(func):
            def wrapper(*arguments, **keywordArguments):
                from threading import Thread
                thr = Thread(target=func, args=arguments, kwargs=keywordArguments)
                if identifier is not None:
                    self._threads[identifier] = thr
                else:
                    self._threads['Generic'].append(thr)


                if autostart is None:
                    if self.autostart:
                        thr.start()
                elif autostart:
                    thr.start()

                return wrapper

        return outer

    def start(self):
        """Starts every thread called"""
        for thr in self._threads.values():
            if isinstance(thr, threading.Thread):
                thr.start()

        for thr in self._threads['Generic']:
            thr.start()

    def join(self):
        """Joins every thread"""
        for thr in self._threads.values():
            if isinstance(thr, threading.Thread):
                thr.join()

        for thr in self._threads['Generic']:
            thr.join()


    @property
    def threads(self):
        """A copy of all the threads ran by the class, threads are stored based on two keys, 'Generic' and the
        identifier passed to the decorator by default if no identifier is passed the thread is stored under the Generic
        array

        i.e.
        {
            'Generic': [Thread1, Thread2, Thread3],
            'Identifier': Thread4,
            'Identifier2': Thread5
        }

        Note: the dictionary is a copy of the original dictionary, not a reference to it
        """
        copy = self._threads
        return copy
