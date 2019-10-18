from django.forms import ModelForm, Textarea, TextInput, FileInput
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

from posts.models import Post


class PostForm(ModelForm):
    class Meta:
       model = Post
       fields = ['name', 'description']
       widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'description': Textarea(attrs={'rows': 10, 'class': 'form-control'}),
        }
