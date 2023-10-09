import json
from groups.models import Groups
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
import threading
# class ChatConsumer(WebsocketConsumer):
#     def connect(self):
#         self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
#         self.room_group_name = f"chat_{self.room_name}"

#         # Join room group
#         async_to_sync(self.channel_layer.group_add)(
#             self.room_group_name, self.channel_name
#         )

#         print(self.room_group_name)
#         print(self.channel_name)
#         print("thread:",threading.get_native_id)
#         self.accept()

#     def disconnect(self, close_code):
#         # Leave room group
#         async_to_sync(self.channel_layer.group_discard)(
#             self.room_group_name, self.channel_name
#         )

#     # Receive message from WebSocket
#     def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json["message"]
#         print("recieve"+str(threading.get_native_id( )))
#         # Send message to room group
#         async_to_sync(self.channel_layer.group_send)(
#             self.room_group_name, {"type": "chat.message", "message": message}
#         )

#     # Receive message from room group
#     def chat_message(self, event):
#         message = event["message"]
#         print("webscoket: "+str(threading.get_native_id()) )
#         # Send message to WebSocket
#         self.send(text_data=json.dumps({"message": message}))


# chat/consumers.py
import json

from channels.generic.websocket import AsyncWebsocketConsumer

from .authentication import LoginAuthentication

class ChatConsumer(AsyncWebsocketConsumer):
    authentication_classes = [LoginAuthentication]
    
    
    
    async def connect(self):

        user = self.scope.get('user')
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        #self.room_group_name lai export garna parcha jastai cha
        print(self.room_name)
        

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat.message", "message": message}
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        print("webscoket: "+str(threading.get_native_id()) )
        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))

    