from django.contrib import admin

from chat.models import Chat, UserProfile, ChatNotification


admin.site.register(Chat)
admin.site.register(UserProfile)
admin.site.register(ChatNotification)
