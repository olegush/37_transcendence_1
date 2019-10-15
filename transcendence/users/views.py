from sentry_sdk import capture_exception
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.forms.models import model_to_dict

from users.models import CustomUser
from .forms import ProfileForm

class DisplayUser(DetailView):
    model = CustomUser
    template_name = 'wall.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = self.object.pk
        me = self.request.user
        context['user'] = get_object_or_404(CustomUser, id = id)
        context['is_friend'] = me.is_authenticated and me.friends.filter(pk=id).exists()
        return context


class UserAddToFriends(UpdateView, LoginRequiredMixin):
    model = CustomUser
    fields = []

    def get_success_url(self, **kwargs):
        user = self.object
        me = get_object_or_404(CustomUser, id=self.request.user.id)
        me.friends.add(user)
        return reverse('user', kwargs={'pk': user.pk})


class UserRemoveFromFriends(UpdateView, LoginRequiredMixin):
    model = CustomUser
    fields = []

    def get_success_url(self, **kwargs):
        user = self.object
        me = get_object_or_404(CustomUser, id=self.request.user.id)
        me.friends.remove(user)
        return reverse('user', kwargs={'pk': user.pk})


class UserUpdate(UpdateView, LoginRequiredMixin):
    model = CustomUser
    form = ProfileForm
    fields = ['name', 'description', 'image']
    template_name = 'profile.html'

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(CustomUser, id = request.user.id)
        form = self.form(initial=model_to_dict(user))
        return render(request, self.template_name, {'form_profile': form})

    def post(self, request, *args, **kwargs):
        #user = get_object_or_404(CustomUser, id = request.user.id)
        form = self.form(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return render(request, self.template_name, {'form_profile': form})
        return render(request, self.template_name, {'form_profile': form, 'pk': user.pk})


class DisplayWall(DetailView, LoginRequiredMixin):
    def get(self, request, *args, **kwargs):
        user = request.user
        return render(request, 'wall.html')
