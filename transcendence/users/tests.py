from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from users.models import CustomUser
from users.forms import ProfileForm


class UserManagersTests(TestCase):
    """Tests for case of creating normal and super user."""

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(email='normal@user.com', password='foo')
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
        admin_user = User.objects.create_superuser('super@user.com', 'foo')
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
    """Tests Post views."""

    def test_all_users_list(self):
        resp_reverse = self.client.get(reverse('users'))
        resp_url = self.client.get('/users/')
        self.assertEqual(resp_reverse.status_code, 200)
        self.assertEqual(resp_url.status_code, 200)

    def test_user_form_update(self):
        user = CustomUser.objects.create(email='user@test.com', name='name', description='description')
        data = {'email': 'email', 'name': 'new name', 'description': 'new description'}
        form = ProfileForm(data=data)
        self.assertTrue(form.is_valid())
