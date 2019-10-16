from sentry_sdk import capture_exception
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, ListView
from django.views.generic.edit import UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.forms.models import model_to_dict
from django.db.models import F, Q, Case, When

from users.models import CustomUser, Post, Status
from .forms import ProfileForm, PostForm

Status.objects.all()
class MyPostsList(LoginRequiredMixin, ListView):
    model = Post
    paginate_by = 10
    template_name = 'my_posts.html'

    def get_queryset(self):
        user_id = self.request.user.id
        return Post.objects.filter(author=user_id)


class SubscriptionsList(LoginRequiredMixin, ListView):
    model = Post
    paginate_by = 10
    template_name = 'subscriptions.html'

    def get_queryset(self):
        user_id = self.request.user.id
        author = CustomUser.objects.get(pk=user_id)
        posts = Post.objects.filter(author__in=author.friends.all())
        return posts.annotate(status__read=F('status__read'))


class AllPostsList(ListView):
    model = Post
    paginate_by = 10
    template_name = 'all_posts.html'

    def get_queryset(self):
        user = self.request.user
        posts = Post.objects.all()
        if user.is_authenticated:
            status_case = Case(When(status__user=user, then='status__read'))
            posts = posts.annotate(status__read=status_case)
        return posts


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        post_id = context['post'].id
        if user.is_authenticated:
            context['readby'] = Status.objects.filter(user=user, post=post_id).first()
        else:
            context['readby'] = 'AnonymousUser'
        return context


class PostListbyAuthor(ListView):
    model = Post
    paginate_by = 10
    template_name = 'post_list_by_author.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.request.user.id
        context['author'] = Author.objects.get(pk=self.kwargs['pk'])
        context['logged_used'] = Author.objects.get(user=user_id)
        return context

    def get_queryset(self):
        author = Author.objects.get(pk=self.kwargs['pk'])
        posts = Post.objects.filter(author=author)
        return posts.annotate(status__read=F('status__read'))


class PostAdd(LoginRequiredMixin, CreateView):
    model = Post
    form = PostForm
    fields = ['name', 'description']
    template_name = 'post_add.html'
    success_url = '/thanks/'

    def get(self, request, *args, **kwargs):
        form = self.form()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        id = request.user.id
        form = self.form(request.POST)
        form.instance.author = CustomUser.objects.get(pk=id)
        if form.is_valid():
            new_post = form.save()
            #TODO !!!!!!!!!
            return redirect('post', pk=new_post.id)
        return render(request, self.template_name, {'form': form, 'pk': request.user.pk})


class PostMarkAsRead(LoginRequiredMixin, CreateView):
    model = Status
    fields = []
    #form = StatusForm

    def form_valid(self, form):
        post_id = self.kwargs['pk']
        user = self.request.user
        read_post = Post.objects.select_related('author').get(pk=post_id)
        Status.objects.create(user=user, post=read_post, read=True)
        return redirect('post', pk=post_id)


class UsersList(ListView):
    model = CustomUser
    paginate_by = 10
    template_name = 'users.html'

    def get_queryset(self):
        return CustomUser.objects.exclude(pk=self.request.user.id)


class UserDisplay(DetailView):
    model = CustomUser
    template_name = 'user.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.request.user.id
        id = self.object.pk
        me = self.request.user
        author = CustomUser.objects.get(pk=id)
        posts = Post.objects.filter(author=author)
        context['posts'] = posts.annotate(status__read=F('status__read'))
        context['user'] = get_object_or_404(CustomUser, id = id)
        context['is_friend'] = me.is_authenticated and me.friends.filter(pk=id).exists()
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
    model = CustomUser
    form = ProfileForm
    fields = ['name', 'description', 'image']
    template_name = 'profile.html'

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(CustomUser, id = request.user.id)
        form = self.form(initial=model_to_dict(user))
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return render(request, self.template_name, {'form': form})
        return render(request, self.template_name, {'form': form, 'pk': user.pk})
