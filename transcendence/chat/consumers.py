import json

from channels.generic.websocket import AsyncWebsocketConsumer

from chat.models import Message, Chat
from users.models import CustomUser


class ChatConsumer(AsyncWebsocketConsumer):
    """Main functions for consumer chat."""

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_name, self.channel_name,
            )

    async def receive(self, text_data):
        user_name = self.scope['user'].name
        user_id = int(self.scope['user'].id)
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        chat = Chat.objects.get(id=int(self.room_name))
        user = CustomUser.objects.get(id=user_id)
        Message.objects.create(chat=chat, user=user, body=message)
        await self.channel_layer.group_send(
            self.room_name,
            {
                'type': 'chat_message',
                'message': f'{user_name} > {message}',
            },
        )

    async def chat_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({'message': message}))
