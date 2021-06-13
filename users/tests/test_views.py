from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class RegisterTest(TestCase):
    def setUp(self):
        self.register_url = reverse('users:register')
        self.user = {
            'username': 'admin',
            'email': 'admin@admin.com',
            'password': 'zoranzoran',
            'confirmation': 'zoranzoran',
        }
        self.user_unmatching_password = {
            'username': 'admin',
            'email': 'admin@admin.com',
            'password': 'zoranzoran',
            'confirmation': 'zoranzoran4',
        }

    def test_can_view_register_page_correctly(self):
        response = self.client.get(self.register_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')

    def test_can_register_user(self):
        response = self.client.post(self.register_url, self.user, format='text/html')

        self.assertEqual(response.status_code, 302)

    def test_cant_register_user_with_unmatching_passwords(self):
        response = self.client.post(self.register_url, self.user_unmatching_password, format='text/html')
        message = response.context['message']

        self.assertEqual(len(message[0]), 1)
        self.assertEqual(str(message), 'Passwords must match.')


class LoginTest(TestCase):

    def setUp(self):
        self.login_url = reverse('users:login')

    def test_can_access_login_page(self):
        response = self.client.get(self.login_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_user_can_login_successfully(self):
        get_user_model().objects.create_user(username='testuser', email='test@test.com', password='12345')
        response = self.client.login(username='testuser', password='12345')

        self.assertTrue(response)

    def test_guest_can_not_login(self):
        response = self.client.login(username='testuser', password='12345')

        self.assertFalse(response)


class LogoutTest(TestCase):
    fixtures = ['users.json']

    def setUp(self):
        self.logout_url = reverse('users:logout')

    def test_logged_in_user_can_logout(self):
        user = get_user_model().objects.get(username='admin-fixture')
        self.client.force_login(user)

        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)
