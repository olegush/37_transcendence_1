from django.forms import ModelForm, Textarea, TextInput, FileInput, HiddenInput
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

from .models import CustomUser


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
            'image': FileInput(attrs={'class': 'form-control', 'data-buttonText': "Your label here."}),
        }
