import socket
import time

from utils2.thread import thread

class ServiceKeys:
    on_connect = "on_connect"
    on_disconnect = "on_disconnect"
    on_receive = "on_receive"
    on_send = "on_send"


class client:
    def __init__(self, sock, address):
        """A simple class to represent the socket and address of a client"""
        self._socket = sock
        self._address = address

    @property
    def address(self):
        return self._address

    @property
    def socket(self):
        return self._socket



def _threadFunction(func):
    """A decorator to run a function in a thread"""
    def wrapper(*args, **kwargs):
        return thread(func, *args, **kwargs)
    return wrapper



class Service(socket.socket):
    def __init__(self, host='0.0.0.0', port=9998, functions=None):
        """
        Fully customizable socket service.

        :param host: The host to listen on.
        :param port: The port to listen on.
        :param functions: A dictionary of functions to call when events occur.
            example:
                {
                    'on_connect': on_connect,
                    'on_disconnect': on_disconnect,
                    'on_receive': on_receive,
                    'on_send': on_send
                }
            Use the ServiceKeys class to get the keys for the dictionary.
            on_connect must be present. it will be passed a Client Class Object.


        """
        self.functions = functions
        # self.bind((host, port))
        super().__init__(socket.AF_INET, socket.SOCK_STREAM)
        self.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.bind((host, port))


        self.threads = {}



        if functions is None:
            self.functions = {}
        else:
            self.functions = {}

        self._alive = True


        assert self.functions.get(ServiceKeys.on_connect) is not None, "on_connect must be present"

    def _get_and_execute(self, key, *args):
        if key in self.functions:
            return self.functions[key](*args)
        else:
            return None

    def _on_connect(self, *args):
        """
        Callback for when a client connects.
        """
        self._get_and_execute(ServiceKeys.on_connect, *args)

    def _on_disconnect(self, *args):
        """
        Callback for when a client disconnects.
        """
        self._get_and_execute(ServiceKeys.on_disconnect, *args)

    def _on_receive(self, *args):
        """
        Callback for when a client sends data.
        """
        self._get_and_execute(ServiceKeys.on_receive, *args)

    def _on_send(self, *args):
        """
        Callback for when a client receives data.
        """
        self._get_and_execute(ServiceKeys.on_send, *args)


    def start_listening(self):
        """
        Starts listening for clients. New clients will be appended to the thread dictionary with the address as the key.
        """
        self.listen()
        while self._alive:
            _client, address = self.accept()
            th = thread(self._on_connect, [client(sock=_client, address=address)])
            self.threads[address] = th


    @_threadFunction
    def _builtin_interceptor(self, connection: socket.socket, address, delay=0.5):
        """
        Builtin interceptor for when a client connects.
        """
        while self._alive:
            time.sleep(delay)
            try:
                data = connection.recv(1024)
                if data:
                    self._on_receive(data, address)
                else:
                    self._on_disconnect(address)
                    break
            except (ConnectionResetError, ConnectionAbortedError, OSError):
                self._on_disconnect(address)
                break

        try:
            connection.close()
        except OSError:
            pass






if __name__ == '__main__':
    s = Service()



