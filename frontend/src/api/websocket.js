const WS_URL = "ws://localhost:8000/ws";


export const createWebSocket = (
    onMessage,
    onOpen,
    onClose
) => {

    const socket = new WebSocket(
        WS_URL
    );


    socket.onopen = () => {

        console.log(
            "WebSocket connected"
        );

        if (onOpen) {
            onOpen();
        }

    };


    socket.onmessage = (event) => {

        const data = JSON.parse(
            event.data
        );

        onMessage(data);

    };


    socket.onclose = () => {

        console.log(
            "WebSocket disconnected"
        );

        if (onClose) {
            onClose();
        }

    };


    socket.onerror = (error) => {

        console.error(
            "WebSocket error:",
            error
        );

    };


    return socket;
};