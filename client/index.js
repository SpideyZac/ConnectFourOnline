const websocket = new WebSocket("ws://localhost:8080/");
websocket.addEventListener("message", ({data}) => {
    console.log(1);
    console.log(JSON.parse(data))
});
websocket.onopen = function() {
    console.log("sent")
    websocket.send(JSON.stringify({"api": "Login", "params": ["1", "2"]}));
}