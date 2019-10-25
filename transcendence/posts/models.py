import pytz

from django.utils import timezone
from django.db import models
from django.urls import reverse

from users.models import CustomUser


class Post(models.Model):
    name = models.CharField(max_length=200)
    author = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    description = models.TextField(max_length=3000)
    bookmarked = models.ManyToManyField(CustomUser, related_name='bookmarked', blank=True, through='Bookmark')
    post_date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-post_date"]

    def get_absolute_url(self):
        return reverse('post', args=[str(self.id)])

    def __str__(self):
        return f'pk: {self.pk}, name: {self.name}, author: {self.author},  description: {self.description},  bookmarked: {self.bookmarked},  post_date: {self.post_date}'


class Bookmark(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, related_name='user')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, related_name='post')
    create_date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-create_date"]

    def __str__(self):
        return f'pk: {self.pk}, user: {self.user}, post: {self.post},  create_date: {self.create_date}'
