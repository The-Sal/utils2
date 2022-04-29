import socket
from utils2.networking import _socketUtils

_serviceKeys = _socketUtils.ServiceKeys
ServiceFunctions = _socketUtils.ServiceFunctions
Client = _socketUtils.client


class Service(socket.socket):
    """A simple wrapper around the socket class that allows for easy creation of a server socket."""
    def __init__(self, functions: ServiceFunctions, host="localhost", port=8080):
        """
        All new connections will be passed to the on_connect function which will be threaded.
        Running threads can be accessed via the 'connections' property. The threads are automatically
        assigned the address of the client as the key. On the __init__ of the class the host and port will bind-ed.


        :param functions: A ServiceFunctions object which is called when key events occur
        :param host: The host to listen on.
        :param port: The port to listen on.

        :type functions: ServiceFunctions
        :type host: str
        :type port: int

        :return: None
        """
        super().__init__(socket.AF_INET, socket.SOCK_STREAM)
        self.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.bind((host, port))

        self._func = functions


        self._alive = True
        self._threads = {}


    def start_listen(self):
        """Starts the service listening for new connections."""
        while self._alive:
            self.listen()
            conn, address = self.accept()

            # check if we have an on_connect function
            on_connect = self._func[_serviceKeys.on_connect]
            if on_connect is None:
                self._threads[address] = _socketUtils.builtinInterceptor(self, conn, address, self._func)
            else:
                self._threads[address] = on_connect(Client(address=address, sock=conn))



    @property
    def connections(self):
        return self._threads

    def stop_listen(self):
        """Stops the service from listening for new connections and closes all connections."""
        self._alive = False
        if len(self.connections) > 0:
            for thread in self._threads.values():
                thread.join()
            self.close()






if __name__ == '__main__':
    pass