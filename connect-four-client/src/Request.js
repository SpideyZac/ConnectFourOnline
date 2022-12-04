const connect = () => {
    const websocket = new WebSocket('ws://localhost:8080/');
    return websocket;
}

const send = (ws, api, params) => {
    ws.send(JSON.stringify({api, params}))
}

export {connect, send}