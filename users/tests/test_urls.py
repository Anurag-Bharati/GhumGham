from django.test import SimpleTestCase
from django.urls import resolve, reverse

from users.views import authenticate, home

class TestUrls(SimpleTestCase):

    # Reverse : retrieve url details from url's.py
    # Resolve : resolving URL paths to the corresponding view functions
    # Assert : func/class == func/class

    def test_auth_url_is_resolved(self):
        url = reverse('auth')
        self.assertEquals(resolve(url).func, authenticate)

    def test_home_url_is_resolved(self):
        url = reverse('home')
        self.assertEquals(resolve(url).func, home)

    def test_account_activated_is_resolved(self):
        pass

    def test_activate_account_is_resolved(self):
        pass

    def test_logout_url_is_resolved(self):
        pass
