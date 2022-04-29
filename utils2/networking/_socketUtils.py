import socket
import time


def thread(func):
    from utils2.threading import thread as __thread

    def wrapper(*args):
        return __thread(func, args=args, daemon=True)

    return wrapper


class ServiceKeys:
    on_connect = "on_connect"
    on_disconnect = "on_disconnect"
    on_receive = "on_receive"
    on_send = "on_send"


class ServiceFunctions:
    def __init__(self, on_connect=None, on_disconnect=None, on_receive=None):
        """
        :param on_connect: function to call when a connection is made to the server


        :param on_disconnect: function to call when a connection is lost to the server.


        :param on_receive: function to call when data is received from the server.

        If the on_connect function is None, them the on_receive and on_disconnect must be defined as they will be
        used by the servers builtin on_connect function called 'builtinInterceptor' which requires the on_disconnect
        and on_receive functions to be defined.

        The on_connect and on_disconnect function is supplied with a single argument which is the 'Client' object
        with the following attributes: Client.address: the address of the client. Client.socket: The actual socket
        object which the client is connected to.

        The on_receive function is supplied with two arguments, the first is the data received from the socket
        (un-decoded) and the second is the Client object.
        """
        self._on_connect = on_connect
        self._on_disconnect = on_disconnect
        self._on_receive = on_receive

    @thread
    def on_connect(self, *args, **kwargs):
        if self._on_connect is not None:
            self._on_connect(*args, **kwargs)

    @thread
    def on_disconnect(self, *args, **kwargs):
        if self._on_disconnect is not None:
            self._on_disconnect(*args, **kwargs)

    @thread
    def on_receive(self, *args, **kwargs):
        if self._on_receive is not None:
            self._on_receive(*args, **kwargs)


    def __getitem__(self, key):
        if key == ServiceKeys.on_connect:
            return self._on_connect
        elif key == ServiceKeys.on_disconnect:
            return self._on_disconnect
        elif key == ServiceKeys.on_receive:
            return self._on_receive
        else:
            return None


class client:
    """A simple class to represent the socket and address of a client"""
    def __init__(self, sock, address):
        self._socket = sock
        self._address = address

    @property
    def address(self):
        return self._address

    @property
    def socket(self):
        return self._socket


@thread
def builtinInterceptor(self, connection: socket.socket, address, functions: ServiceFunctions, buff=1024):
    """
    This is the builtin interceptor for the Server class. it requires that all associated functions of the
    ServiceFunctions class be passed defined.
    """

    try:
        assert functions[ServiceKeys.on_receive] is not None, "on_receive must be defined"
        assert functions[ServiceKeys.on_disconnect] is not None, "on_disconnect must be defined"
    except Exception as err:
        connection.close()
        raise err

    while self._alive:
        time.sleep(0.3)

        try:
            data = connection.recv(buff)
            if data:
                functions.on_receive(data, client(connection, address))
            else:
                functions.on_disconnect(client(connection, address))
                break

        except (ConnectionResetError, ConnectionAbortedError, OSError):
            functions.on_disconnect(client(connection, address))

            try:
                connection.close()
            except OSError:
                pass

            break
