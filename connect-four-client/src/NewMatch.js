import { useEffect, useState } from "react";
import { useParams, useHistory, Link } from "react-router-dom";
import { send } from "./Request";

const NewMatch = ({ websocket }) => {
    const history = useHistory();
    const { username, token } = useParams();
    const [player2, setPlayer2] = useState('');
    const [failedMessage, setFailedMessage] = useState(null);
    const [gameID, setGameID] = useState(null);
    
    useEffect(() => {
        websocket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            if (!data.result) {
                history.push("/");
            }
        }
        send(websocket, "IsKeyLinked", [token, username]);
    }, []);

    const handleSubmit = (e) => {
        e.preventDefault();
        const params = [token, username, player2];

        websocket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            if (data.success) {
                setGameID(data.id);
            } else {
                setFailedMessage(data.error);
            }
        }
        send(websocket, "CreateNewGame", params);
    }

    if (gameID === null) {
        return (
            <div className="new-match-form">
                <h2>Create New Match</h2>
                {failedMessage && <p>{failedMessage}</p>}
                <form onSubmit={handleSubmit}>
                    <label>Player 2's Username</label>
                    <input type="text" required value={player2} onChange={(e) => setPlayer2(e.target.value)} />
                    <button>Create New Match</button>
                </form>
                <br></br>
                <h3>PLEASE USE THE LINK BELOW SO YOU DON'T GET LOGGED OUT</h3>
                <Link to={`/redirect/${username}/${token}`}>Back to the Main Menu</Link>
            </div>
        );
    } else {
        return (
            <div className="new-match-form">
                <h2>Created New Match</h2>
                <h3>Your Game ID is: {gameID}</h3>
                <br></br>
                <h3>PLEASE USE THE LINK BELOW SO YOU DON'T GET LOGGED OUT</h3>
                <Link to={`/redirect/${username}/${token}`}>Back to the Main Menu</Link>
            </div>
        );
    }
}
 
export default NewMatch;