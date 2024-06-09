console.log("hi");
const socket = new WebSocket('ws://' + window.location.host + `/ws/waiting_room/${game_id}/`);

var $chatBox;
var maxPlayers;
var currentPlayers;

$(function() {
    $chatBox = $("#chat-messages-container");
    maxPlayers = parseInt($("#max_players_input").val());
    currentPlayers = parseInt($("#current_players_joined_input").val());

    $("#start-game-button").on('click', function() {
        socket.send(JSON.stringify({
            'type': 'start_game'
        }));
    });

    $("#end-game-button").on('click', function() {
        socket.send(JSON.stringify({
            'type': 'end_game'
        }));
        window.location.href = "/home";
    });

    $("#leave-game-button").on('click', function() {
        socket.close();
        window.location.href = "/home";
    });
    
})

socket.onopen = function() {
    console.log('Connected to the server');
};

socket.onclose = function() {
    console.log('Disconnected from the server');
};

socket.onmessage = function(event) {
    console.log("Message recevied");
    var data = JSON.parse(event.data);
    console.log(event);
    console.log(data);

    $chatBox.append(`<div class="chat-message">${data.message}</div>`);

    if (data.type == "new_user") {
        currentPlayers += 1;
        $("#players-joined-label").text(`Players joined: ${currentPlayers}/${maxPlayers}`);
        if (currentPlayers >= 2) {
            $("#start-game-button").prop('disabled', false);
        }
        $("#players-joined-list").append(`<li>${data.username}</li>`);
    }
    else if (data.type == "user_exit") {
        currentPlayers -= 1;
        $("#players-joined-label").text(`Players joined: ${currentPlayers}/${maxPlayers}`);
        if (currentPlayers < 2) {
            $("#start-game-button").prop('disabled', true);
        }
        $("#players-joined-list li").filter(function() {
            return $(this).text() == data.username;
        }).remove();
    }

    else if (data.type == "start_game") {
        window.location.href = "/game/" + game_id;
    }

    else if (data.type == "end_game") {
        window.location.href = "/home";
    }
    
}