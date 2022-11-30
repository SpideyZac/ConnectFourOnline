const websocket = new WebSocket("ws://localhost:8080/");
websocket.addEventListener("message", ({data}) => {
    console.log(JSON.parse(data))
    //websocket.close(1000)
    websocket.close()
});
websocket.onopen = function() {
    console.log("sent")
    websocket.send(JSON.stringify({"api": "Signup", "params": ["test", "test", "test", "test"]}));
}