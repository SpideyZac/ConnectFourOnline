import { useEffect, useState } from "react";
import { useParams, useHistory, Link } from "react-router-dom";
import board from "./images/board.png";
import black_token from "./images/black-token.png";
import red_token from "./images/red-token.png";
import { send } from "./Request";

const JoinMatch = ({ websocket }) => {
    const history = useHistory();
    const { username, token } = useParams();
    const [gameID, setGameID] = useState('');
    const [gameValidated, setGameValidated] = useState(false);
    const [failedMessage, setFailedMessage] = useState(null);
    const [gameState, setGameState] = useState(null);
    const [team, setTeam] = useState(null);
    const [interval, setUInterval] = useState(null);
    const [gameOver, setGameOver] = useState(false);
    const [message, setMessage] = useState(null);

    useEffect(() => {
        websocket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            if (!data.result) {
                history.push("/");
            }
        }
        send(websocket, "IsKeyLinked", [token, username]);

        return () => {if (interval) clearInterval(interval)};
    }, []);

    const updater = () => {
        websocket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            const game = JSON.parse(data.game[3]);

            if (game.turn === team) {
                clearInterval(interval);
            }

            setGameState(game);

            if (game.finished === 1) {
                setGameOver(true);
                if (game.tied) {
                    setMessage("Game Over... You Tied!");
                } else if (game.winner === team) {
                    setMessage("Game Over... You Won!");
                } else {
                    setMessage("Game Over... You Lost!");
                }
            }
        }
        setUInterval(setInterval(() => {
            send(websocket, "ViewGame", [gameID]);
        }, 5000));
    }

    const handleSubmit = (e) => {
        e.preventDefault();
        const params = [token, username, gameID];

        websocket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            if (data.success) {
                setFailedMessage(null);
                setGameValidated(true);
                setTeam(data.team);

                websocket.onmessage = (event) => {
                    const data2 = JSON.parse(event.data);
                    const game = JSON.parse(data2.game[3]);
                    setGameState(game);
                    if (game.finished === 1) {
                        setGameOver(true);
                        if (game.tied) {
                            setMessage("Game Over... You Tied!");
                        } else if (game.winner === data.team) {
                            setMessage("Game Over... You Won!");
                        } else {
                            setMessage("Game Over... You Lost!");
                        }
                    } else {
                        updater();
                    }
                }
                send(websocket, "ViewGame", [gameID]);
            } else {
                setFailedMessage(data.error);
            }
        }
        send(websocket, "GetTeam", params);
    }

    if (!gameValidated) {
        return (
            <div className="join-match">
                <h2>Join Match</h2>
                {failedMessage}
                <form onSubmit={handleSubmit}>
                    <label>Game ID</label>
                    <input type="text" required value={gameID} onChange={(e) => setGameID(e.target.value)} />
                    <button>Join Game</button>
                </form>
                <br></br>
                <h3>PLEASE USE THE LINK BELOW SO YOU DON'T GET LOGGED OUT</h3>
                <Link to={`/redirect/${username}/${token}`}>Back to the Main Menu</Link>
            </div>
        );
    } else {
        const column_open = (index) => {
            return gameState.column_spots[index] >= 0;
        }

        const make_move = (index) => {
            const params = [token, username, gameID, index + 1];

            websocket.onmessage = (event) => {
                const data = JSON.parse(event.data);
                if (data.success) {
                    setFailedMessage(null);
                    setGameState(JSON.parse(data.state));
                    updater();
                } else {
                    setFailedMessage(data.error);
                }
            }
            send(websocket, "MakeMove", params);
        }

        const render_board = () => {
            return gameState.board.map((row, index) => {
                return row.map((column, ind) => {
                    if (column !== 0) {
                        if (column === 1) {
                            return (<img src={red_token} alt="Red Token" key={index * 7 + ind} style={{
                                    position: "absolute",
                                    zIndex: -1,
                                    left: (-155 + ind * 85),
                                    top: (30 + index * 85),
                                    marginRight: "auto",
                                    marginLeft: "auto",
                                    width: "400px",
                            }} />);
                        } else {
                            return (<img src={black_token} alt="Black Token" key={index * 7 + ind} style={{
                                position: "absolute",
                                zIndex: -1,
                                left: (-155 + ind * 85),
                                top: (31 + index * 85),
                                marginRight: "auto",
                                marginLeft: "auto",
                                width: "400px",
                            }} />);
                        }
                    }
                });
            });
        }

        const draw_buttons = () => {
            return gameState.board[0].map((column, index) => {
                return (
                    <button onClick={() => {make_move(index)}} key={index} className={column_open(index) && gameState.turn === team ? "ready" : "dis"}></button>
                );
            });
        }

        if (gameState) {
            if (!gameOver) {
                if (gameState.turn === team) {
                    return (
                        <div className="game">
                            {failedMessage}
                            <br></br>
                            {draw_buttons()}
                            {render_board()}
                            <img src={board} alt="Connect Four Board" />
                            <br></br>
                            <h3>PLEASE USE THE LINK BELOW SO YOU DON'T GET LOGGED OUT</h3>
                            <Link to={`/redirect/${username}/${token}`}>Back to the Main Menu</Link>
                        </div>
                    );
                } else {
                    return (
                        <div className="game">
                            {failedMessage}
                            <br></br>
                            {draw_buttons()}
                            {render_board()}
                            <img src={board} alt="Connect Four Board" />
                            <br></br>
                            <h3>PLEASE USE THE LINK BELOW SO YOU DON'T GET LOGGED OUT</h3>
                            <Link to={`/redirect/${username}/${token}`}>Back to the Main Menu</Link>
                        </div>
                    );
                }
            } else {
                return (
                    <div className="game-over">
                        <p>{message}</p>
                        <h3>PLEASE USE THE LINK BELOW SO YOU DON'T GET LOGGED OUT</h3>
                        <Link to={`/redirect/${username}/${token}`}>Back to the Main Menu</Link>
                    </div>
                );
            }
        }
    }
}
 
export default JoinMatch;