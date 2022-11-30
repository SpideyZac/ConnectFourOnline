# Imports
import asyncio
from websockets import serve
import json
import sqlite3
import random
import string

# Database
database_connection = sqlite3.connect("connectfour.db", check_same_thread=False)

database_connection.execute("CREATE TABLE IF NOT EXISTS players (id INT UNSIGNED NOT NULL, username TEXT NOT NULL, firstname TEXT NOT NULL, lastname TEXT NOT NULL, password TEXT NOT NULL)")
database_connection.execute("CREATE TABLE IF NOT EXISTS games (id INT UNSIGNED NOT NULL, whiteplayerid INT UNSIGNED NOT NULL, redplayerid INT UNSIGNED NOT NULL, state TEXT NOT NULL)")

# Player verification keys
pvk = {}
verification_keys_in_use = []
conn_to_key = {}

# API Functions
def signup(parameters: list, conn) -> dict:
    if len(parameters) < 4:
        return {"success": False, "error": "Not enough parameters"}

    username = parameters[0]
    firstname = parameters[1]
    lastname = parameters[2]
    password = parameters[3]

    if not isinstance(username, str):
        return {"success": False, "error": "Username must be a string"}
    if not isinstance(firstname, str):
        return {"success": False, "error": "First Name must be a string"}
    if not isinstance(lastname, str):
        return {"success": False, "error": "Last Name must be a string"}
    if not isinstance(password, str):
        return {"success": False, "error": "Password must be a string"}

    c = database_connection.cursor()

    if c.execute("SELECT * FROM players WHERE username=?", (username,)).fetchone() is None:
        c.execute("INSERT INTO players (id, username, firstname, lastname, password) VALUES (?, ?, ?, ?, ?)", (
            len(c.execute("SELECT * FROM players").fetchall()),
            username,
            firstname,
            lastname,
            password
        ))
        database_connection.commit()
        c.close()

        verification_key = "".join(random.choice(string.digits) for _ in range(50))
        while verification_key in verification_keys_in_use:
            verification_key = "".join(random.choice(string.digits) for _ in range(50))
        pvk[verification_key] = username
        conn_to_key[conn] = verification_key

        return {"success": True, "verification_key": verification_key}
    else:
        c.close()
        return {"success": False, "error": "That username is already in use"}

def login(parameters: list, conn) -> dict:
    if len(parameters) < 2:
        return {"success": False, "error": "Not enough parameters"}

    username = parameters[0]
    password = parameters[1]

    if username in pvk:
        return {"success": False, "error": "That user is already logged in"}

    c = database_connection.cursor()
    if c.execute("SELECT * FROM players WHERE username=? AND password=?", (username, password)).fetchone() is not None:
        verification_key = "".join(random.choice(string.digits) for _ in range(50))
        while verification_key in verification_keys_in_use:
            verification_key = "".join(random.choice(string.digits) for _ in range(50))

        if conn in conn_to_key:
            key = conn_to_key[conn]
            pvk.pop(key)
            print(f"Removed Verification Key: {key}")

        pvk[verification_key] = username
        conn_to_key[conn] = verification_key

        c.close()
        return {"success": True, "verification_key": verification_key}
    else:
        c.close()
        return {"success": False, "error": "That is not a valid user or not the correct password"}

def createNewGame(parameters: list, conn) -> dict:
    if len(parameters) < 2:
        return {"success": False, "error": "Not enough parameters"}

    # Player Verification Key Check
    if parameters[0] not in pvk:
        return {"success": False, "error": "Invalid verification key passed"}

    player1_username = pvk[parameters[0]]
    player2_username = parameters[1]

    c = database_connection.cursor()

    # check if players usernames are the same
    if player1_username == player2_username:
        c.close()
        return {"success": False, "error": "Players cannot be the same"}

    # check if players exist
    player1_entry = c.execute("SELECT * FROM players WHERE username=?", (player1_username,)).fetchone()
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

    return {"success": True, "state": state, "team": 1, "id": game_id}

def viewGame(parameters: list, conn) -> dict:
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

def getTeam(parameters: list, conn) -> dict:
    if len(parameters) < 2:
        return {"success": False, "error": "Not enough parameters"}

    if parameters[1] not in pvk:
        return {"success": False, "error": "Invalid verification key passed"}

    gameId = parameters[0]
    player_username = pvk[parameters[1]]

    c = database_connection.cursor()

    game = c.execute("SELECT * FROM games WHERE id=?", (gameId,)).fetchone()
    if game is None:
        c.close()
        return {"success": False, "error": "Game does not exist"}

    player = c.execute("SELECT * FROM players WHERE username=?", (player_username,)).fetchone()
    if game[1] != player[0] and game[2] != player[0]:
        c.close()
        return {"success": False, "error": "That user is not in that game"}
    elif game[1] == player[0]:
        c.close()
        return {"success": True, "team": 1}
    else:
        c.close()
        return {"success": True, "team": -1}

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

def makeMove(parameters: list, conn) -> dict:
    if len(parameters) < 3:
        return {"success": False, "error": "Not enough parameters"}

    game_id = parameters[0]

    # Player Verification Key Check
    if parameters[1] not in pvk:
        return {"success": False, "error": "Invalid verification key passed"}

    playername = pvk[parameters[1]]
    # we subtract 1 because column is an index
    if not isinstance(parameters[2], int):
        return {"success": False, "error": "Column must be a int"}
    column = parameters[2] - 1

    c = database_connection.cursor()

    player = c.execute("SELECT * FROM players WHERE username=?", (playername,)).fetchone()

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

    return {"success": True, "state": state, "team": team}

# API Handles
apis = {
    "CreateNewGame": createNewGame,
    "ViewGame": viewGame,
    "MakeMove": makeMove,
    "Signup": signup,
    "Login": login,
    "GetTeam": getTeam,
}

# Socket Server
async def start_server():
    async with serve(socket_thread, "localhost", 8080):
        await asyncio.Future()

# Socket User Handler
async def socket_thread(conn):
    print("Connect")
    try:
        async for data in conn:
            # Data should be in structure:
            # {
            #    api: str with the name of the api to call
            #    params: list with the parameters to the api
            # }
            try:
                json_data = json.loads(data)

                if "api" not in json_data:
                    await conn.send(json.dumps({"success": False, "error": "Request missing api str"}))
                elif "params" not in json_data:
                    await conn.send(json.dumps({"success": False, "error": "Request missing params list"}))
                else:
                    if json_data["api"] in apis:
                        if isinstance(json_data["params"], list):
                            await conn.send(json.dumps(apis[json_data["api"]](json_data["params"], conn)))
                        else:
                            await conn.send(json.dumps({"success": False, "error": "Params must be of type list"}))
                    else:
                        await conn.send(json.dumps({"success": False, "error": "API requested is not valid"}))
            except json.JSONDecodeError:
                await conn.send(json.dumps({"success": False, "error": "Data must be of type: JSON"}))
    except:
        pass

    print("Disconnect")
    if conn in conn_to_key:
        # disconnect
        key = conn_to_key.pop(conn)
        pvk.pop(key)

if __name__ == "__main__":
    asyncio.run(start_server())