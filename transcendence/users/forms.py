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


class ProfileForm(forms.ModelForm):
    class Meta:
       model = CustomUser
       fields = ['name', 'description']
    #name = forms.CharField(label='Your name', max_length=200)
    #image = forms.ImageField(label='image')
    #description = forms.CharField(widget=forms.Textarea)
