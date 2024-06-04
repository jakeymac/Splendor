from django.urls import path, include
from Game import views as game_views


urlpatterns = [
    path("game", game_views.game_page),
    path("home", game_views.home, name="home"),
    path("new_game", game_views.new_game, name="new_game"),
    path("create_game", game_views.create_game, name="create_game"),
]