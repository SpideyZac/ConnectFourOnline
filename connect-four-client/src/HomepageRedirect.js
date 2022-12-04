import { useEffect } from "react";
import { useHistory, useParams } from "react-router-dom";
import { send } from "./Request";
import Main from "./Main";

const HomepageRedirect = ({ websocket }) => {
    const history = useHistory();
    const { username, token } = useParams();

    useEffect(() => {
        websocket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            if (!data.result) {
                history.push("/");
            }
        }
        send(websocket, "IsKeyLinked", [token, username]);
    }, []);

    return (
        <Main websocket={websocket} username={username} token={token} />
    );
}
 
export default HomepageRedirect;