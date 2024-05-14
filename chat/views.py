from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import get_user_model

from chat.models import Chat


User = get_user_model()

def index(request):
    users = User.objects.exclude(username=request.user.username)
    return render(request, 'index.html', {'users': users})


def chatPage(request, username):
    user = User.objects.get(username=username)
    users = User.objects.exclude(username=request.user.username)
    
    if request.user.id > user.id:
        thread_name = f"chat_{request.user.id}-{user.id}"
    else:
        thread_name = f"chat_{user.id}-{request.user.id}"
    messages = Chat.objects.filter(thread_name=thread_name)
    return render(request, 'main_chat.html', {'users': users, 'user': user, 'messages': messages})