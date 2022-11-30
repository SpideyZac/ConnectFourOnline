const websocket = new WebSocket("ws://localhost:8080/");
websocket.onopen = function() {
    console.log(websocket.send(JSON.stringify({"api": "Login", "params": ["1", "2"]})));
    websocket.close();
}