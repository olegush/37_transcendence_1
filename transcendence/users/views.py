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
    return render(request, 'wall.html', context={'user': {'is_authenticated': is_authenticated, 'name': user.name, 'description': user.description, 'image': user.image}})


@login_required
def show_profile(request):
    if request.method == 'POST':
        user = get_object_or_404(CustomUser, id = request.user.id)
        form = ProfileForm(request.POST, instance=user)
        if form.is_valid():

            #print(user)
            form.save()
            #user.name =
            return render(request, 'profile.html', context={'user': request.user, 'form': form})
    else:
        data = {'name': request.user.name, 'description': request.user.description}
        form = ProfileForm(data)
    return render(request, 'profile.html', context={'user': request.user, 'form': form})
