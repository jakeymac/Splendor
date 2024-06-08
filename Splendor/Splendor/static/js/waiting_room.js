console.log("hi");
const socket = new WebSocket('ws://' + window.location.host + `/ws/waiting_room/${game_id}/`);
socket.onopen = function() {
    console.log('Connected to the server');
};

socket.onclose = function() {
    console.log('Disconnected from the server');
};

socket.onmessage = function(event) {
    console.log("Message recevied");
    const data = JSON.parse(event.data);
    console.log(event);
    console.log(data);
    if (data.type == "new_user") {
        console.log("User entered");
    }
}