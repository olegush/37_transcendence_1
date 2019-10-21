from django.forms import ModelForm, Textarea, TextInput
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from users.models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """Create custom user."""

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):
    """Edit custom user."""

    class Meta:
        model = CustomUser
        fields = ('email',)


class ProfileForm(ModelForm):
    """Edit user info."""

    class Meta:
        model = CustomUser
        fields = ['name', 'description', 'image']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'description': Textarea(attrs={'rows': 10, 'class': 'form-control'}),
            }
