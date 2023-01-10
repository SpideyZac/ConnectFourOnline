import { useHistory } from "react-router-dom";

const Main = ({ websocket, username, token }) => {
    const history = useHistory();

    const handleNewMatch = () => {
        history.push(`/newmatch/${username}/${token}`);
    }

    const handleJoinMatch = () => {
        history.push(`/joinmatch/${username}/${token}`);
    }

    return (
        <div className="main">
            <h2>Welcome, {username}!</h2>
            <p>This is your homepage</p>
            <br></br>
            <button onClick={handleNewMatch}>New Match</button>
            <br></br>
            <br></br>
            <button onClick={handleJoinMatch}>Join Game</button>
        </div>
    );
}
 
export default Main;