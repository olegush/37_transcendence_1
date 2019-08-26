from sentry_sdk import capture_exception
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from users.models import CustomUser
from .forms import ProfileForm


def display_user(request, **kwargs):
    id = kwargs['user_id']
    user = get_object_or_404(CustomUser, id = id)
    if request.method == 'POST':
        request.user.friends.add(user)
    is_friend = request.user.is_authenticated and request.user.friends.filter(pk=id).exists()
    return render(request, 'wall.html', context={'is_friend': is_friend, 'user': user})


@login_required
def display_wall(request):
    user = request.user
    return render(request, 'wall.html', context={'user': user})


@login_required
def display_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
    user = get_object_or_404(CustomUser, id = request.user.id)
    form = ProfileForm({'name': user.name, 'description': user.description, 'image': user.image})
    return render(request, 'profile.html', context={'user': user, 'form': form.as_p})
