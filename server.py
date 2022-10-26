# Imports
import socket
import _thread
import json
import sqlite3

# Database
database_connection = sqlite3.connect("connectfour.db", check_same_thread=False)

database_connection.execute("CREATE TABLE IF NOT EXISTS players (id INT UNSIGNED NOT NULL, username TEXT NOT NULL, firstname TEXT NOT NULL, lastname TEXT NOT NULL)")
database_connection.execute("CREATE TABLE IF NOT EXISTS games (id INT UNSIGNED NOT NULL, whiteplayerid INT UNSIGNED NOT NULL, redplayerid INT UNSIGNED NOT NULL, state TEXT NOT NULL)")

# Constants
HOST = socket.gethostname()
PORT = 8080

print(HOST, PORT)

# API Functions
def CreateNewGame(parameters: list) -> dict:
    if len(parameters) < 2:
        return {"success": False, "error": "Not enough parameters"}

    c = database_connection.cursor()

    player1_username = parameters[0]
    player2_username = parameters[1]

    # check if players usernames are the same
    if player1_username == player2_username:
        c.close()
        return {"success": False, "error": "Players cannot be the same"}

    # check if players exist
    player1_entry = c.execute("SELECT * FROM players WHERE username=?", (player1_username,)).fetchone()
    if player1_entry is None:
        c.close()
        return {"success": False, "error": "Player1 was not found"}
    player2_entry = c.execute("SELECT * FROM players WHERE username=?", (player2_username,)).fetchone()
    if player2_entry is None:
        c.close()
        return {"success": False, "error": "Player2 was not found"}

    # generate game id
    game_id = len(c.execute("SELECT * FROM games").fetchall())

    # create new game and insert into database
    state = {}

    state["board"] = [[0 for _ in range(7)] for _ in range(6)]
    state["column_spots"] = [5 for _ in range(7)]
    state["turn"] = 1
    state["finished"] = 0
    state["winner"] = 0
    state["tied"] = False

    state = json.dumps(state)

    c.execute("INSERT INTO games (id, whiteplayerid, redplayerid, state) VALUES (?, ?, ?, ?)", (game_id, player1_entry[0], player2_entry[0], state))

    database_connection.commit()
    c.close()

    return {"success": True, "state": state, "id": game_id}

def ViewGame(parameters: list) -> dict:
    if len(parameters) < 1:
        return {"success": False, "error": "Not enough parameters"}

    c = database_connection.cursor()

    # get game with id
    game = c.execute("SELECT * FROM games WHERE id=?", (parameters[0],)).fetchone()

    if game is None:
        c.close()
        return {"success": False, "error": "Game does not exist"}

    c.close()

    return {"success": True, "game": game}

def updateGameState(state: dict, column: int) -> dict:
    state["board"][state["column_spots"][column]][column] = state["turn"]
    row = state["column_spots"][column]
    state["column_spots"][column] -= 1

    won = False
    # downward
    if row + 3 < 6:
        if state["board"][row + 1][column] == state["turn"] and state["board"][row + 2][column] == state["turn"] and state["board"][row + 3][column] == state["turn"]:
            state["winner"] = state["turn"]
            won = True
    if not won:
        # right
        if column + 3 < 7:
            if state["board"][row][column + 1] == state["turn"] and state["board"][row][column + 2] == state["turn"] and state["board"][row][column + 3] == state["turn"]:
                state["winner"] = state["turn"]
                won = True
    if not won:
        # left
        if column - 3 >= 0:
            if state["board"][row][column - 1] == state["turn"] and state["board"][row][column - 2] == state["turn"] and state["board"][row][column - 3] == state["turn"]:
                state["winner"] = state["turn"]
                won = True
    if not won:
        # diaganol right
        if row + 3 < 6 and column + 3 < 7:
            if state["board"][row + 1][column + 1] == state["turn"] and state["board"][row + 2][column + 2] == state["turn"] and state["board"][row + 3][column + 3] == state["turn"]:
                state["winner"] = state["turn"]
                won = True
    if not won:
        # diaganol left
        if row + 3 < 6 and column - 3 >= 0:
            if state["board"][row + 1][column - 1] == state["turn"] and state["board"][row + 2][column - 2] == state["turn"] and state["board"][row + 3][column - 3] == state["turn"]:
                state["winner"] = state["turn"]
                won = True
    if not won:
        # tie
        for cs in state["column_spots"]:
            if cs != -1:
                break
        else:
            won = True
            state["tied"] = True
    
    if won:
        state["finished"] = 1

    state["turn"] *= -1

    return state

def MakeMove(parameters: list) -> dict:
    if len(parameters) < 3:
        return {"success": False, "error": "Not enough parameters"}

    c = database_connection.cursor()

    game_id = parameters[0]
    playername = parameters[1]
    # we subtract 1 because column is an index
    column = parameters[2] - 1

    player = c.execute("SELECT * FROM players WHERE username=?", (playername,)).fetchone()
    if player is None:
        c.close()
        return {"success": False, "error": "That player is not found"}

    game = c.execute("SELECT * FROM games WHERE id=?", (game_id,)).fetchone()
    if game is None:
        c.close()
        return {"success": False, "error": "That game is not found"}

    if column < 0 or column > 6:
        c.close()
        return {"success": False, "error": "The column is out of range... should be 1-7 including 1 and 7"}

    if game[1] != player[0] and game[2] != player[0]:
        c.close()
        return {"success": False, "error": "That user is not in that game"}
    elif game[1] == player[0]:
        team = 1
    else:
        team = -1

    state = json.loads(game[3])

    if state["finished"] != 0:
        c.close()
        return {"success": False, "error": "That game is already finished", "winner": state["winner"], "tied": state["tied"]}

    if state["turn"] != team:
        c.close()
        return {"success": False, "error": "It is not your turn"}

    if state["column_spots"][column] == -1:
        c.close()
        return {"success": False, "error": "That column is already full"}

    # process new game state
    state = json.dumps(updateGameState(state, column))
    c.execute("UPDATE games SET state=? WHERE id=?", (state, game_id))
    database_connection.commit()
    c.close()

    return {"success": True, "state": state}

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
            except json.JSONDecodeError:
                conn.send('Data must be of type: JSON'.encode())
        except socket.error:
            print(f"Disconnect by {addr}")
            break

if __name__ == "__main__":
    start_server()