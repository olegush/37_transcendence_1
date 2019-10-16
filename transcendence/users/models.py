from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    name = models.CharField('name', max_length=200, default='')
    image = models.ImageField('image', upload_to='avatars', null=True, blank=True)
    description = models.TextField('description', blank=True, default='')
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    friends = models.ManyToManyField('self', symmetrical=False, verbose_name="friends", related_name="my_friends", blank=True)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return '{}: {}'.format(self.id, self.email)

    def get_absolute_url(self):
        return reverse('user', kwargs={'pk': self.pk})


class Post(models.Model):
    name = models.CharField(max_length=200)
    author = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    description = models.TextField(max_length=3000)
    post_date = models.DateTimeField(default=datetime.now)

    class Meta:
        ordering = ["-post_date"]

    def get_absolute_url(self):
        return reverse('post', args=[str(self.id)])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        user = CustomUser.objects.get(id = self.author_id)
        subject = f'New post added by {user}'
        message = f'{user} just added <a href="/blog/post/{self.id}/">new post</a>'
        # TODO !!!
        #recipient_list = [author.email  for author in CustomUser.objects.all() if user in author.friends.all()]
        #send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list )

    def __str__(self):
        return f'{self.pk}'


class Status(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    read = models.BooleanField(default=True)

    def __str__(self):
        return f'pk: {self.pk}, user: {self.user}, post: {self.post}, read: {self.read}'
