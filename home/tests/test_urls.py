from django.test import SimpleTestCase
from django.urls import reverse,resolve
from home.views import *


class TestUrls(SimpleTestCase):
    def test_admindashboard_urls_is_resolved(self):
        url=reverse('homepage')
        view=resolve(url).func
        self.assertEquals(view,homepage)
