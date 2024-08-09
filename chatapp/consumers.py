import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from app.models import Room, Message, User

# Update ChatConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        self.user = self.scope["user"]

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

        # Notify room that a user has joined
        await self.channel_layer.group_send(
            self.room_group_name, {
                'type': 'user_joined',
                'username': self.user.username,
            }
        )

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action')

        if action == 'message':
            await self.handle_message(data)
        elif action == 'mark_as_read':
            await self.handle_mark_as_read(data)

    async def handle_message(self, data):
        message = data['message']
        username = data['username']
        room_name = data['room_name']

        await self.save_message(message, username, room_name)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {
                'type': 'chat_message',
                'message': message,
                'username': username,
            }
        )

    async def handle_mark_as_read(self, data):
        message_ids = data['message_ids']
        await self.mark_messages_as_read(message_ids)

    async def user_joined(self, event):
        username = event['username']
        # Notify all clients in the room
        await self.channel_layer.group_send(
            self.room_group_name, {
                'type': 'user_joined_event',
                'username': username,
            }
        )

    async def user_joined_event(self, event):
        username = event['username']
        await self.send(text_data=json.dumps({
            'action': 'user_joined',
            'username': username,
        }))

    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
        }))

    @sync_to_async
    def save_message(self, message, username, room_name):
        user = User.objects.get(username=username)
        room = Room.objects.filter(slug=room_name).first()
        Message.objects.create(user=user, room=room, content=message)

    @sync_to_async
    def mark_messages_as_read(self, message_ids):
        Message.objects.filter(id__in=message_ids).update(is_read=True)

    @sync_to_async
    def mark_message_as_read(self, message_content):
        Message.objects.filter(content=message_content).update(is_read=True)
