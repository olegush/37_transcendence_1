from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.shortcuts import render
from django.utils.safestring import mark_safe
import json
from users.models import CustomUser


def index(request):
    return render(request, 'chat/index.html', {})


class ChatRoom(LoginRequiredMixin, View):
    """Chat Room."""

    template_name = 'chat/room.html'

    def get(self, request, *args, **kwargs):
        ids = sorted([kwargs['id1'], kwargs['id2']])
        room_name = '{}_{}'.format(ids[0], ids[1])
        return render(request, self.template_name, {
            'room_name_json': mark_safe(json.dumps(room_name)),
        })
