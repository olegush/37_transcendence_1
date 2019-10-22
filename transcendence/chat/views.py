from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
import json
from users.models import CustomUser


class ChatsList(LoginRequiredMixin, View):

    #model = Chat
    template_name = 'chat/list.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class ChatRoom(LoginRequiredMixin, View):
    """Chat Room."""

    template_name = 'chat/room.html'

    def get(self, request, *args, **kwargs):
        ids = sorted([kwargs['id1'], kwargs['id2']])
        if self.request.user.id not in ids:
            return redirect('chats')
        room_name = '{}_{}'.format(ids[0], ids[1])
        ids.remove(int(self.request.user.id))
        chat_with = CustomUser.objects.get(id=ids[0]).name
        return render(request, self.template_name, {
            'room_name_json': mark_safe(json.dumps(room_name)),
            'chat_with': mark_safe(json.dumps(chat_with)),
        })
