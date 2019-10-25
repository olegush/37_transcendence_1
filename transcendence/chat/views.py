import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.shortcuts import render
from django.db.models import Count

from users.models import CustomUser
from chat.models import Chat, Message


class ChatsList(LoginRequiredMixin, View):
    """Chat List."""

    template_name = 'chat/list.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class ChatRoom(LoginRequiredMixin, View):
    """Chat Room for two users.

    Easy to scale for multiuser chat without changing the mode.

    """

    template_name = 'chat/room.html'

    def get(self, request, *args, **kwargs):
        me = CustomUser.objects.get(id=self.request.user.id)
        user_to_chat = CustomUser.objects.get(id=kwargs['id'])
        chatting_users = [me, user_to_chat]
        room = Chat.objects.annotate(Count('users'))
        room = room.filter(users__count=len(chatting_users))
        for user in chatting_users:
            room = room.filter(users__id=user.id)
        if room:
            room = room.get()
        else:
            room = Chat.objects.create()
            for user in chatting_users:
                room.users.add(user)
        messages = Message.objects.filter(chat=room)
        return render(request, self.template_name, {
            'room_name_json': json.dumps(room.id),
            'chat_with': json.dumps(user_to_chat.name),
            'messages': messages,
        })
