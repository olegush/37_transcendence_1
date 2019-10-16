from django.forms import ModelForm, Textarea, TextInput, FileInput
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

from .models import CustomUser, Post


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email',)


class ProfileForm(ModelForm):
    class Meta:
       model = CustomUser
       fields = ['name', 'description', 'image']
       widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'description': Textarea(attrs={'rows': 10, 'class': 'form-control'}),
        }

class PostForm(ModelForm):
    class Meta:
       model = Post
       fields = ['name', 'description']
       widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'description': Textarea(attrs={'rows': 10, 'class': 'form-control'}),
        }
