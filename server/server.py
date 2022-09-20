# Imports
import socket
import _thread
import json

# Constants
HOST = "0.0.0.0"
PORT = 8080

# API Functions
def CreateNewGame(parameters: list) -> str:
    if len(parameters) != 2:
        return {"success": False}

    return {"success": True, "data": "Hi"}

# API Handles
apis = {
    "CreateNewGame": CreateNewGame
}

# Socket Server
def start_server():
    socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_server.bind((HOST, PORT))
    socket_server.listen()

    while True:
        conn, addr = socket_server.accept()
        print(f"Connect by {addr}")
        _thread.start_new_thread(socket_thread, (conn, addr))

# Socket User Handler
def socket_thread(conn: socket.socket, addr: socket._RetAddress):
    while True:
        try:
            data = conn.recv(1024)
            # Data should be in structure:
            # {
            #    api: str with the name of the api to call
            #    params: list with the parameters to the api
            # }
            try:
                json_data = json.loads(data)
                if 'api' not in json_data:
                    conn.send('Request missing api str'.encode())
                elif 'params' not in json_data:
                    conn.send('Request missing params list'.encode())
                else:
                    if json_data['api'] in apis:
                        conn.send(apis[json_data['api']](json_data['params']).encode())
                    else:
                        conn.send('API requested is not valid'.encode())
            except:
                conn.send('Data must be of type: JSON'.encode())
        except:
            break