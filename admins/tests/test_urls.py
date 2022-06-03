from django.test import SimpleTestCase
from django.urls import reverse,resolve
from admins.views import *


class TestUrls(SimpleTestCase):
    def test_show_packages_urls_is_resolved(self):
        url=reverse('show_packages')
        view=resolve(url).func
        self.assertEquals(view,showpackages)

    def test_add_packages_urls_is_resolved(self):
        url=reverse('addpackages')
        view=resolve(url).func
        self.assertEquals(view,addpackages)

    
    def test_delete_package_urls_is_resolved(self):
        url=reverse('packages_delete', args=['2'])
        view=resolve(url).func
        self.assertEquals(view,packages_delete)

    def test_update_packages_urls_is_resolved(self):
        url=reverse('update_packages', args=['3'])
        view=resolve(url).func
        self.assertEquals(view,update_packages)

    def test_admin_urls_is_resolved(self):
        url=reverse('admin',)
        view=resolve(url).func
        self.assertEquals(view,admin)





    