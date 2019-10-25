from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.conf import settings

from users.models import CustomUser
from posts.models import Post, Bookmark
from posts.forms import PostForm


class MyPostsList(LoginRequiredMixin, ListView):
    """Display user's posts list."""

    model = Post
    paginate_by = 10
    template_name = 'posts/my_posts.html'

    def get_queryset(self):
        user_id = self.request.user.id
        return Post.objects.filter(author=user_id)


class SubscriptionsList(LoginRequiredMixin, ListView):
    """Display user's subscriptions list."""

    model = Post
    paginate_by = 10
    template_name = 'posts/subscriptions.html'

    def get_queryset(self):
        user = self.request.user
        author = CustomUser.objects.get(pk=user.id)
        return Post.objects.filter(author__in=author.friends.all())


class BookmarksList(LoginRequiredMixin, ListView):
    """Display user's bookmarks list."""

    model = Post
    paginate_by = 10
    template_name = 'posts/bookmarks.html'

    def get_queryset(self):
        user = self.request.user
        return Bookmark.objects.filter(user=user)


class AllPostsList(ListView):
    """Display all posts list."""

    model = Post
    paginate_by = 10
    template_name = 'posts/all_posts.html'

    def get_queryset(self):
        return Post.objects.all()


class PostDetail(LoginRequiredMixin, DetailView):
    """Display detailed post with bookmark button."""

    model = Post
    template_name = 'posts/post.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        post_id = context['post'].id
        context['bookmarked'] = Bookmark.objects.filter(
            user=user, post=post_id,
            ).first()
        return context


class PostAdd(LoginRequiredMixin, CreateView):
    """A new post.

    Adds a new post and redirects to post page.

    """

    model = Post
    form = PostForm
    fields = ['name', 'description']
    template_name = 'posts/post_add.html'

    def get(self, request, *args, **kwargs):
        form = self.form()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        user_id = request.user.id
        user_name = request.user.name
        form = self.form(request.POST)
        form.instance.author = CustomUser.objects.get(pk=user_id)
        if form.is_valid():
            new_post = form.save()
            subject = f'New post added by {user_name}'
            message = f'{user_name} just added <a href="/blog/post/{new_post.id}/">new post</a>'
            recipient_list = [author.email  for author in CustomUser.objects.all() if request.user in author.friends.all()]
            send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)
            return redirect('post', pk=new_post.id)
        return render(
            request, self.template_name, {'form': form, 'pk': request.user.pk},
            )


class PostToBookmark(LoginRequiredMixin, CreateView):
    """Adds a post to user's bookmarks."""

    model = Bookmark
    fields = []

    def form_valid(self, form):
        post_id = self.kwargs['pk']
        user = self.request.user
        post = get_object_or_404(Post, id=post_id)
        post.bookmarked.add(user)
        return redirect('post', pk=post_id)
