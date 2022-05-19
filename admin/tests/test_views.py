from django.test import TestCase, Client
from django.urls import reverse

class TestViews(TestCase):


         # @classmethod
        # def setUpTestData(cls):
        #         cls.client = Client()
        #         cls.dashboard_url = reverse('dashboard')
           

        # def test_dashboard(self):    
        #         response=self.client.get(self.dashboard_url)
        #         self.assertTemplateUsed(response,'admins_home.html')

        def test_homepage(self):    
                response=self.client.get(reverse('admindashboard'))
                self.assertTemplateUsed(response,'admins_home.html')
        

        