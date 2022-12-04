import { useState } from 'react';
import { Link, useHistory } from "react-router-dom";
import { send } from './Request';

const Login = ({ websocket }) => {
    const [username, setUsername] = useState('');
    const [firstname, setFirstname] = useState('');
    const [lastname, setLastname] = useState('');
    const [password, setPassword] = useState('');
    const [failed, setFailed] = useState(false);
    const history = useHistory();

    const handleSubmit = (e) => {
        e.preventDefault();
        const params = [username, firstname, lastname, password];
        
        websocket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            if (data.success) {
                history.push('/');
            } else {
                setFailed(true);
            }
        }
        send(websocket, "Signup", params);
    }

    return (
        <div className="signup">
            <h2>Signup</h2>
            {failed && <p>You could not signup because the username is taken</p>}
            <form onSubmit={handleSubmit}>
                <label>Username</label>
                <input type="text" required value={username} onChange={(e) => setUsername(e.target.value)} />
                <label>First Name</label>
                <input type="text" required value={firstname} onChange={(e) => setFirstname(e.target.value)} />
                <label>Last Name</label>
                <input type="text" required value={lastname} onChange={(e) => setLastname(e.target.value)} />
                <label>Password</label>
                <input type="password" required value={password} onChange={(e) => setPassword(e.target.value)} />
                <button>Signup</button>
            </form>
            <br></br>
            <Link to="/">Need to login?</Link>
        </div>
    );
}
 
export default Login;