from django.forms import ModelForm, Textarea, TextInput, FileInput

from posts.models import Post


class PostForm(ModelForm):
    """Create user post."""

    class Meta:
        model = Post
        fields = ['name', 'description']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'description': Textarea(attrs={'rows': 10, 'class': 'form-control'}),
            }
