import { send } from "./Request";
import Login from "./Login";
import Main from "./Main";

const Home = ({ websocket }) => {
    const login_comp = Login({websocket});
    if (login_comp.username) {
        const { username, key } = login_comp;
        return (
            <Main websocket={websocket} username={username} token={key} />
        );
    } else {
        send(websocket, "Signout", []);
        return login_comp;
    }
}
 
export default Home;