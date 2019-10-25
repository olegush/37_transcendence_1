import pytz

from django.utils import timezone
from django.db import models
from users.models import CustomUser


class Chat(models.Model):
    users = models.ManyToManyField(
        CustomUser, related_name='related_users', blank=True,
        )
    create_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.pk} {self.users} {self.create_date}'


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    body = models.TextField('body', blank=True, default='')
    send_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.pk}'
