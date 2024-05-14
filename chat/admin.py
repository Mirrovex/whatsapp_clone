from django.contrib import admin

from chat.models import Chat, UserProfile


admin.site.register(Chat)
admin.site.register(UserProfile)
