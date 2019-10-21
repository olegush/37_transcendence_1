from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from users.models import CustomUser
from users.forms import ProfileForm


class UserManagersTests(TestCase):
    """Tests for case of creating normal and super user."""

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user('normal@user.com', 'pwd12345')
        self.assertEqual(user.email, 'normal@user.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertEqual(user.get_absolute_url(), f'/id{user.id}/')
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(user.username)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email='')
        with self.assertRaises(ValueError):
            User.objects.create_user(email='', password='foo')

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser('super@user.com', 'pwd12345')
        self.assertEqual(admin_user.email, 'super@user.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(admin_user.username)
        except AttributeError:
            pass
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email='super@user.com', password='foo', is_superuser=False,
                )


class UserViewsTests(TestCase):
    """Tests User views."""

    def test_redirect_if_not_logged_in(self):
        resp_profile = self.client.get(reverse('profile'))
        self.assertRedirects(resp_profile, '/accounts/login/?next=/profile/')

    def test_all_users_list(self):
        resp_reverse = self.client.get(reverse('users'))
        resp_url = self.client.get('/users/')
        self.assertEqual(resp_reverse.status_code, 200)
        self.assertEqual(resp_url.status_code, 200)

    def test_user_form_update(self):
        form = ProfileForm(
            data={'name': 'new name', 'description': 'new description'},
            )
        self.assertTrue(form.is_valid())

    def test_user_add_to_friends(self):
        user = CustomUser.objects.create(
            email='user@test.com',
            name='name',
            description='description',
            )
        friend = CustomUser.objects.create(
            email='friend@test.com',
            name='friend name',
            description='friend description',
            )
        friend2 = CustomUser.objects.create(
            email='friend2@test.com',
            name='friend name',
            description='friend description',
            )
        user.friends.add(friend)
        user = CustomUser.objects.get(email='user@test.com')
        self.assertTrue(friend in user.friends.all())
        self.assertFalse(friend2 in user.friends.all())

    def test_user_remove_from_friends(self):
        user = CustomUser.objects.create(
            email='user@test.com',
            name='name',
            description='description',
            )
        friend = CustomUser.objects.create(
            email='friend@test.com',
            name='friend name',
            description='friend description',
            )
        user.friends.add(friend)
        user = CustomUser.objects.get(email='user@test.com')
        user.friends.remove(friend)
        self.assertFalse(friend in user.friends.all())
