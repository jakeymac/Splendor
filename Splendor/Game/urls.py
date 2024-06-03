from django.urls import path, include
from Game import views as game_views


urlpatterns = [
    path("game", game_views.game_page),
    path("home", game_views.home, name="home"),
]