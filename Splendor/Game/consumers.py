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

    async def disconnect(self, close_code):
        print("Disconnected from waiting room")
        waiting_room = await database_sync_to_async(WaitingRoom.objects.get)(game_id=self.game_id)
        await database_sync_to_async(waiting_room.remove_player)(self.scope['user'].id)

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_exit',
                'message': 'User has exited'
            }
        )
        
        await self.leave_waiting_room()

    async def new_user(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))

    async def user_exit(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))
        

    async def broadcast_new_user(self):
        print("Hi")
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'new_user',
                'message': 'New user joined the waiting room'
            }
        )

    async def broadcast_user_exit(self):
        print("Left")
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_exit',
                'message' : 'User has left the waiting room'
            }
        )

    async def add_to_waiting_room(self):
        waiting_room = await database_sync_to_async(WaitingRoom.objects.get)(game_id=self.game_id)
        await database_sync_to_async(waiting_room.add_player)(self.scope['user'].id)
        await database_sync_to_async(waiting_room.save)()
        await self.broadcast_new_user()
        
        
    async def leave_waiting_room(self):
        waiting_room = await database_sync_to_async(WaitingRoom.objects.get)(game_id=self.game_id)
        await database_sync_to_async(waiting_room.remove_player)(self.scope['user'].id)
        await database_sync_to_async(waiting_room.save)()
        await self.broadcast_user_exit()

    def close_waiting_room(self):
        game_id = self.scope['url_route']['kwargs']['game_id']
        waiting_room = WaitingRoom.objects.get(game_id=game_id)
        waiting_room.delete()



        
        

    

    
