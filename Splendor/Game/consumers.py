import json
from channels.generic.websocket import AsyncWebsocketConsumer

from channels.db import database_sync_to_async

from .models import WaitingRoom

class WaitingRoomConsumer(AsyncWebsocketConsumer):
    players = set()

    async def connect(self):
        print("Connected to waiting room")
        self.game_id = self.scope['url_route']['kwargs']['game_id']
        self.room_group_name = 'waiting_room_%s' % self.game_id

        await self.channel_layer.group_add(
            self.room_group_name, 
            self.channel_name
        )
        await self.accept()
        await self.add_to_waiting_room()
        await self.broadcast_new_user()

    async def disconnect(self, close_code):
        print("Disconnected from waiting room")
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
                
        await self.leave_waiting_room()
        await self.broadcast_user_exit()

    async def receive(self, text_data):
        print("Received message: ", text_data)
        type = json.loads(text_data)['type']
        if type == 'start_game':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'start_game',
                    'message': 'Game is starting'
                }
            )
            await self.close_waiting_room()

        elif type == "end_game":
           
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'end_game',
                    'message': 'Game has ended'
                }
            )
            await self.close_waiting_room()

    async def new_user(self, event):
        print("New user function")
        message = event['message']
        username = event['username']
        await self.send(text_data=json.dumps({
            "type": "new_user",
            'message': message,
            "username": username
        }))

    async def user_exit(self, event):
        print("User exit function")
        message = event['message']
        username = event['username']
        await self.send(text_data=json.dumps({
            "type": "user_exit",
            'message': message,
            "username": username
        }))

    async def start_game(self, event):
        print("Start game function")
        message = event['message']
        await self.send(text_data=json.dumps({
            "type": "start_game",
            'message': message
        }))

    async def end_game(self, event):
        print("End game function")
        message = event['message']
        await self.send(text_data=json.dumps({
            "type": "end_game",
            'message': message
        }))
        
    async def broadcast_new_user(self):
        print("Broacasting new user")
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'new_user',
                'message': f"{self.scope['user'].username} joined the waiting room",
                "username": self.scope['user'].username
            }
        )

    async def broadcast_user_exit(self):
        print("Braodcast user exits ")
        print("Left")
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_exit',
                'message' : 'User has left the waiting room',
                'username': self.scope['user'].username
            }
        )

    async def add_to_waiting_room(self):
        print("Running add to waiting room")
        waiting_room = await database_sync_to_async(WaitingRoom.objects.get)(game_id=self.game_id)
        await database_sync_to_async(waiting_room.add_player)(self.scope['user'].id)
        
        
    async def leave_waiting_room(self):
        print("leave waiting room function")
        try:
            waiting_room = await database_sync_to_async(WaitingRoom.objects.get)(game_id=self.game_id)
            await database_sync_to_async(waiting_room.remove_player)(self.scope['user'].id)
        except:
            pass
        
    async def close_waiting_room(self):
        print("Close waiting room")
        game_id = self.scope['url_route']['kwargs']['game_id']
        waiting_room = await database_sync_to_async(WaitingRoom.objects.get)(game_id=game_id)
        await database_sync_to_async(waiting_room.delete)()

