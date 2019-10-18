from sentry_sdk import capture_exception
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, ListView
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.forms.models import model_to_dict

from users.models import CustomUser
from posts.models import Post
from users.forms import ProfileForm


class UsersList(ListView):
    model = CustomUser
    paginate_by = 10
    template_name = 'users/users.html'

    def get_queryset(self):
        return CustomUser.objects.exclude(pk=self.request.user.id)


class UserDisplay(DetailView):
    model = CustomUser
    template_name = 'users/user.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.object.pk
        me = self.request.user
        posts = Post.objects.filter(author=CustomUser.objects.get(pk=user_id))
        context['posts'] = posts
        context['user'] = get_object_or_404(CustomUser, id=user_id)
        context['is_friend'] = me.is_authenticated and me.friends.filter(pk=user_id).exists()
        return context


class UserAddToFriends(LoginRequiredMixin, UpdateView):
    model = CustomUser
    fields = []

    def get_success_url(self, **kwargs):
        user = self.object
        me = get_object_or_404(CustomUser, id=self.request.user.id)
        me.friends.add(user)
        return reverse('user', kwargs={'pk': user.pk})


class UserRemoveFromFriends(LoginRequiredMixin, UpdateView):
    model = CustomUser
    fields = []

    def get_success_url(self, **kwargs):
        user = self.object
        me = get_object_or_404(CustomUser, id=self.request.user.id)
        me.friends.remove(user)
        return reverse('user', kwargs={'pk': user.pk})


class UserUpdate(LoginRequiredMixin, UpdateView):
    """Updates user."""

    model = CustomUser
    form = ProfileForm
    fields = ['name', 'description', 'image']
    template_name = 'users/profile.html'

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(CustomUser, id=request.user.id)
        form = self.form(initial=model_to_dict(user))
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return render(request, self.template_name, {'form': form})
        return render(
            request, self.template_name, {'form': form, 'pk': request.user.pk},
            )
