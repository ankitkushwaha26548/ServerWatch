const API_URL = import.meta.env.VITE_API_URL || `${window.location.protocol}//${window.location.hostname}:8000`;
const WS_URL = API_URL.replace(/^http/, "ws") + "/ws";


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
