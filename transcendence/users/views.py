from sentry_sdk import capture_exception
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from users.models import CustomUser
from .forms import ProfileForm


def show_user(request, **kwargs):
    is_authenticated = request.user.is_authenticated
    if kwargs:
        user = get_object_or_404(CustomUser, id = kwargs['user_id'])
    else:
        user = request.user
    friends = [{'id':friend.id, 'name': friend.name} for friend in user.friends.all()]
    return render(request, 'wall.html', context={'user': {'is_authenticated': is_authenticated, 'name': user.name, 'description': user.description, 'image': user.image, 'friends': friends}})


@login_required
def show_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
    user = get_object_or_404(CustomUser, id = request.user.id)
    form = ProfileForm({'name': user.name, 'description': user.description, 'image': user.image})
    return render(request, 'profile.html', context={'user': user, 'form': form.as_p})
