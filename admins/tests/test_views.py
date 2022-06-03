from ast import arg
from importlib.resources import Package
from django.test import TestCase,Client
from django.urls import reverse

from packages.models import Packages


class Test_views(TestCase):
    def test_admin_get(self):
        client=Client()
        response=client.get(reverse('admin'))
        self.assertTemplateUsed(response,'admins_home.html')

    def test_showpackages_get(self):
        client=Client()
        response=client.get(reverse('show_packages'))
        self.assertTemplateUsed(response,'packages.html')

    def test_add_packages_get(self):
        client=Client()
        response=client.get(reverse('addpackages'))
        self.assertTemplateUsed(response,'add_packages.html')

    # def test_update_packages_get(self):
    #     client=Client()
    #     packages=Packages()
    #     packages.cover_pick=1
    #     packages.is_featured=False
    #     packages.save()
    #     response=client.get(reverse('update_packages',args=['0']))
    #     self.assertTemplateUsed(response,'update_packages.html')

    # def test_add_packages_get(self):
    #     client=Client()
    #     response=client.get(reverse('packages_delete'))
    #     self.assertTemplateUsed(response,'')

    # def test_home_page(self):
    #     client=Client()
    #     response=client.get(reverse('packages_delete',args=['2']))
    #     self.assertEquals(response.status_code, 302)
    #     self.assertRedirects(response, '/admin/packages')