from django.test import SimpleTestCase
from django.urls import reverse, resolve
from users.views import LoginView, RegisterView, LogoutView


class TestUrls(SimpleTestCase):

    def test_login_url_resolves(self):
        url = reverse('users:login')
        self.assertEqual(resolve(url).func.view_class, LoginView)

    def test_register_url_resolves(self):
        url = reverse('users:register')
        self.assertEqual(resolve(url).func.view_class, RegisterView)

    def test_logout_url_resolves(self):
        url = reverse('users:logout')
        self.assertEqual(resolve(url).func.view_class, LogoutView)