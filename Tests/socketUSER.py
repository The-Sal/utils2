from utils2.networking import sockets
from utils2.threading import thread


def test_on_recv(data: bytes, client: sockets.Client):
    print("Received:", data.decode(), "from", client.address[0])
    client.socket.send(data)


def test_on_disconnect(client: sockets.Client):
    print("Client disconnected:", client.address[0])

# on_receive=test_on_recv, on_disconnect=test_on_disconnect
service_functions = sockets.ServiceFunctions(on_receive=test_on_recv, on_disconnect=test_on_disconnect)
service = sockets.Service(service_functions)
service2 = sockets.Service(service_functions)
thread(service2.start_listen)
print(service2.connections)
