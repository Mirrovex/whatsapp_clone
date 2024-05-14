from django.db.models.signals import post_save
from django.dispatch import receiver

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json

from chat.models import UserProfile, ChatNotification


@receiver(post_save, sender=UserProfile)
def send_onlineStatus(sender, instance, created, **kwargs):
    if not created:
        channel_layer = get_channel_layer()
        user = instance.user.username
        user_status = instance.online_status

        data = {
            'username': user,
            'status': user_status
        }

        async_to_sync(channel_layer.group_send)(
            'user', {
                'type': 'send_onlineStatus',
                'value': json.dumps(data)
            }
        )


@receiver(post_save, sender=ChatNotification)
def send_notification(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        notification = ChatNotification.objects.filter(is_seen=False, user=instance.user).count()
        user_id = str(instance.user.id)
        data = {
            'count': notification
        }

        async_to_sync(channel_layer.group_send)(
            user_id, {
                'type': 'send_notification',
                'value': json.dumps(data)
            }
        )