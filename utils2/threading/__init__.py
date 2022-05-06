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

    def __init__(self, autostart=False, daemon=False):
        """
        Decorate whatever function with the class to add it to the que of threads
        i.e.
        threadPool = ThreadPool()

        @threadPool()
        def function(*args, **kwargs):
            print('Hello World')

        @threadPool(autostart=False)
        def function2(*args, **kwargs):
            print('Hello World')


        function() -- This function will now run in a thread when called
        function2() -- This function will not run in a thread when called it requires the threadPool.start() to be
        called

        note: The threadPool.start() will start every not-alie thread ever wrapped by @threadPool() and called.



        :param autostart: Defines if the threads should be started automatically or stored as a Thread object to be
            called later
        """
        self.daemon = daemon
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
                thr = Thread(target=func, args=arguments, kwargs=keywordArguments, daemon=self.daemon)
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
        """Starts every thread called, runtime errors are ignored as threads which are already
        been started will be called again"""
        for thr in self._threads.values():
            if isinstance(thr, threading.Thread):
                if not thr.is_alive():
                    try:
                        thr.start()
                    except RuntimeError:
                        pass

        for thr in self._threads['Generic']:
            try:
                thr.start()
            except RuntimeError:
                pass

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


if __name__ == '__main__':
    pool = ThreadPool(autostart=True)


    @pool()
    def function(*args, **kwargs):
        print('Hello World')


    @pool(identifier='Identifier', autostart=False)
    def function2(*args, **kwargs):
        print('Hello World2')


    function()
    function2()

    pool.start()

    print(pool.threads)