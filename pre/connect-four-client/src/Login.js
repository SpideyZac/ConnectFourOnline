import { useState } from 'react';
import { Link } from "react-router-dom";
import { send } from './Request';

const Login = ({ websocket }) => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [key, setKey] = useState('');
    const [sendResponse, setSendResponse] = useState(false);
    const [failed, setFailed] = useState(false);

    const handleSubmit = (e) => {
        e.preventDefault();
        const params = [username, password];
        
        websocket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            if (data.success) {
                setKey(data.verification_key);
                setSendResponse(true);
            } else {
                setFailed(true);
            }
        }
        send(websocket, "Login", params);
    }
    if (sendResponse) {
        return {username, key};
    }

    return (
        <div className="login">
            <h2>Login</h2>
            {failed && <p>Those credentials did not work!</p>}
            <form onSubmit={handleSubmit}>
                <label>Username</label>
                <input type="text" required value={username} onChange={(e) => setUsername(e.target.value)} />
                <label>Password</label>
                <input type="password" required value={password} onChange={(e) => setPassword(e.target.value)} />
                <button>Login</button>
            </form>
            <br></br>
            <Link to="/signup">Need to signup?</Link>
        </div>
    );
}
 
export default Login;