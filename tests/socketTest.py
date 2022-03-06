import random
import socket
import time

s = socket.socket()
host = socket.gethostname()
port = 8080

s.connect(("localhost", port))
while True:
    s.sendall('Hello, world {}'.format(random.random()).encode())
    print(s.recv(1024).decode())

    time.sleep(2)

    s.sendall('vroom {}'.format(random.random()).encode())
    print(s.recv(1024).decode())
