from django.urls import path , include, re_path
from Game.consumers import WaitingRoomConsumer

# Here, "" is routing to the URL ChatConsumer which 
# will handle the chat functionality.
websocket_urlpatterns = [ 
    re_path(r'ws/waiting_room/(?P<game_id>\w+)/$', WaitingRoomConsumer.as_asgi()),
] 