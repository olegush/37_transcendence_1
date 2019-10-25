from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from users.managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """Custom user model."""

    email = models.EmailField(_('email address'), unique=True)
    name = models.CharField('name', max_length=200, default='')
    image = models.ImageField(
        'image', upload_to='avatars', null=True, blank=True,
        )
    description = models.TextField('description', blank=True, default='')
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    friends = models.ManyToManyField(
        'self',
        symmetrical=False,
        verbose_name='friends',
        related_name='my_friends',
        blank=True,
        )

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f'{self.pk}: {self.email}'

    def get_absolute_url(self):
        return reverse('user', kwargs={'pk': self.pk})
