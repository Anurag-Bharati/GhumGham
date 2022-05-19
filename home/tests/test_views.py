from django.test import TestCase, Client
from django.urls import reverse

class TestViews(TestCase):



        def test_homepage(self):    
                response=self.client.get(reverse('homepage'))
                self.assertTemplateUsed(response,'index.html')
        

        