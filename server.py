# Imports
import socket
import _thread
import json
import mysql.connector
import dotenv
import os

dotenv.load_dotenv()

# MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd=os.getenv("PASSWORD"),
    database="connectfouronline"
)

# Constants
HOST = socket.gethostname()
PORT = 8080

print(HOST, PORT)

# API Functions
def CreateNewGame(parameters: list) -> dict:
    if len(parameters) < 2:
        return {"success": False}

    return {"success": True, "data": "Hi"}

def ViewGame(parameters: list) -> dict:
    if len(parameters) < 1:
        return {"success": False}

    return {"success": True, "data": "Hi"}

def MakeMove(parameters: list) -> dict:
    if len(parameters) < 3:
        return {"success": False}

    return {"success": True, "data": "Hi"}

# API Handles
apis = {
    "CreateNewGame": CreateNewGame,
    "ViewGame": ViewGame,
    "MakeMove": MakeMove,
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
def socket_thread(conn: socket.socket, addr):
    while True:
        try:
            data = conn.recv(1024).decode()
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
                        if isinstance(json_data['params'], list):
                            conn.send(json.dumps(apis[json_data['api']](json_data['params'])).encode())
                        else:
                            conn.send('Params must be of type list'.encode())
                    else:
                        conn.send('API requested is not valid'.encode())
            except:
                conn.send('Data must be of type: JSON'.encode())
        except:
            print(f"Disconnect by {addr}")
            break

if __name__ == "__main__":
    start_server()