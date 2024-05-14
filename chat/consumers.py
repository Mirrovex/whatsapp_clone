import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from chat.models import Chat, UserProfile
from django.contrib.auth.models import User


class PersonalChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        current_user_id = self.scope["user"].id
        other_user_id = self.scope["url_route"]["kwargs"]["id"]
        if int(current_user_id) > int(other_user_id):
            self.room_name = f"{current_user_id}-{other_user_id}"
        else:
            self.room_name = f"{other_user_id}-{current_user_id}"

        self.room_group_name = f"chat_{self.room_name}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, code):
        self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, byte_data=None):
        data = json.loads(text_data)
        message = data["message"]
        username = data["username"]

        await self.save_message(username, self.room_group_name, message)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "username": username
            }
        )

    async def chat_message(self, event):
        message = event["message"]
        username = event["username"]

        await self.send(text_data=json.dumps({
            "message": message,
            "username": username
        }))

    @database_sync_to_async
    def save_message(self, username, thread_name, message):
        Chat.objects.create(sender=username, message=message, thread_name=thread_name)


class OnlineStatusConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_group_name = 'user'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, message):
        self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        username = data["username"]
        connection_type = data["type"]

        await self.change_online_status(username, connection_type)

    async def send_onlineStatus(self, event):
        data = json.loads(event.get("value"))
        username = data["username"]
        online_status = data["status"]
        
        await self.send(text_data=json.dumps({
            'username': username,
            'online_status': online_status
        }))

    @database_sync_to_async
    def change_online_status(self, username, c_type):
        user = User.objects.get(username=username)
        userprofile = UserProfile.objects.get(user=user)
        
        userprofile.online_status = c_type == 'open'
        userprofile.save(update_fields=["online_status"])