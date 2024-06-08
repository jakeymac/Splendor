$(function() {
    $("#join-game-form").on("submit", function(event) {
        event.preventDefault();
        const formData = new FormData(this);
        let game_id = formData.get("game_id");
        window.location.href = `/join_game/${game_id}`;
    })
});