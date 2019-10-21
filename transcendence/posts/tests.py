from django.urls import reverse
from django.test import TestCase

from users.models import CustomUser
from posts.models import Post, Bookmark
from posts.forms import PostForm


class PostModelTests(TestCase):
    """Tests for model Post."""

    def test_post_creation(self):
        author = CustomUser.objects.create(email='user@test.com', name='user')
        post =  Post.objects.create(name='post 1', author=author, description='description post')
        self.assertEqual(post.name, 'post 1')
        self.assertEqual(post.description, 'description post')
        self.assertEqual(post.get_absolute_url(), f'/post/{post.id}/')


class BookmarkModelTests(TestCase):
    """Tests for model Bookmark."""

    def test_bookmark_creation(self):
        author = CustomUser.objects.create(email='user@test.com', name='user')
        post = Post.objects.create(name='post 1', author=author, description='description post')
        bookmark = Bookmark.objects.create(user=author, post=post)
        self.assertEqual(bookmark.user, author)
        self.assertEqual(bookmark.post, post)


class PostViewsTests(TestCase):
    """Tests Post views."""

    def setUp(self):
        number_of_posts = 17
        author = CustomUser.objects.create(email='user@test.com', name='user')
        author.set_password('Pwd-12345')
        author.save()
        for post_num in range(number_of_posts):
            Post.objects.create(
                name=f'post #{post_num}',
                author=author,
                description=f'description for post #{post_num}',
                )

    def test_all_posts_list(self):
        resp_reverse = self.client.get(reverse('all-posts'))
        resp_url = self.client.get('/all_posts/')
        self.assertEqual(resp_reverse.status_code, 200)
        self.assertEqual(resp_url.status_code, 200)

    def test_redirect_if_not_logged_in(self):
        resp_my_posts = self.client.get(reverse('my-posts'))
        resp_subscriptions = self.client.get(reverse('subscriptions'))
        resp_bookmarks = self.client.get(reverse('bookmarks'))
        self.assertRedirects(resp_my_posts, '/accounts/login/?next=/my_posts/')
        self.assertRedirects(
            resp_subscriptions, '/accounts/login/?next=/subscriptions/',
            )
        self.assertRedirects(resp_bookmarks, '/accounts/login/?next=/bookmarks/')

    def test_my_posts_list(self):
        login = self.client.login(email='user@test.com', password='Pwd-12345')
        resp_my_posts = self.client.get(reverse('my-posts'))
        resp_subscriptions = self.client.get(reverse('subscriptions'))
        resp_bookmarks = self.client.get(reverse('bookmarks'))
        self.assertEqual(str(resp_my_posts.context['user']), 'user@test.com')
        self.assertEqual(resp_my_posts.status_code, 200)
        self.assertEqual(str(resp_subscriptions.context['user']), 'user@test.com')
        self.assertEqual(resp_subscriptions.status_code, 200)
        self.assertEqual(str(resp_bookmarks.context['user']), 'user@test.com')
        self.assertEqual(resp_bookmarks.status_code, 200)

    def test_form_post_adding(self):
        author = CustomUser.objects.get(email='user@test.com')
        post = Post.objects.create(
            name='post 1', author=author, description='description post',
            )
        form = PostForm(
            data={'name': post.name, 'description': post.description},
            )
        self.assertTrue(form.is_valid())
