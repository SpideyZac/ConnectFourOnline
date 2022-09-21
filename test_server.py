import socket
import json

HOST = socket.gethostname()
PORT = 8080

tests = [
    {
        'api': "Login",
        'params': ["e"],
    }
]

socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

socket_client.connect((HOST, PORT))

for test in tests:
    socket_client.send(json.dumps(test).encode())
    print(socket_client.recv(1024).decode())

socket_client.close()