from django.urls import path, include
from Game import views as game_views


urlpatterns = [
    path("home", game_views.home, name="home"),
    path("new_game", game_views.new_game, name="new_game"),
    path("create_game", game_views.create_game, name="create_game"),
    path("join_game/<str:game_id>", game_views.join_waiting_room, name="join_waiting_room"),
    path("game/<str:game_id>/", game_views.join_game, name="game"),
]