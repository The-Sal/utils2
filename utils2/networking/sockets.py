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
        Access to the connection threads can be accessed via the 'connections' property. The threads are automatically
        assigned the address of the client as the key.


        :param functions: A dictionary of functions to be used by the service.
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
        for thread in self._threads.values():
            thread.join()
        self.close()


    def __del__(self):
        self.stop_listen()




if __name__ == '__main__':
    import time

    def test_on_recv(data: bytes, client: Client):
        print("Received:", data.decode(), "from", client.address[0])
        client.socket.send(data)

    def test_on_disconnect(client: Client):
        print("Client disconnected:", client.address[0])

    funcs = ServiceFunctions(on_receive=test_on_recv, on_disconnect=test_on_disconnect)
    s = Service(functions=funcs)
    s.start_listen()
    time.sleep(5)
    s.stop_listen()
    print(s.connections)
