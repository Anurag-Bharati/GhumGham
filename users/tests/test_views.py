from django.test import TestCase, Client
from django.urls import reverse

from users.models import User
from users.views import checkPass


def create_user(name="test_customer", email="test_customer", is_staff=False, is_active=True):
    user = User.objects.create(username=name)
    user.set_password('123456')
    user.email = email
    user.is_active = is_active
    if is_staff:
        user.is_customer = False
        user.is_staff = True
    user.save()
    return user

class TestViews(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.user = create_user()
        cls.auth_page_url = reverse('auth')

    def setUp(self):
        pass

    def test_auth_page(self):
        response = self.client.get(self.auth_page_url)
        self.assertEquals(response.status_code, 200)

    def test_activated_page(self):
        pass

    def test_logout(self):
        pass

    def test_user_login(self):

        # Valid Case
        response = self.client.post(self.auth_page_url, {
            'username': self.user.username,
            'password': '123456'
        })
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/')

    def test_user_reg(self):
        # Valid Case
        response = self.client.post(self.auth_page_url, {
            'username': self.user.username+"1",
            'password': '123456Aa',
            'email': 'thisisfroaproject@gmail.com',
            'address': 'Lol'
        })

        self.assertEquals(response.status_code, 200)

    def test_check_pass(self):
        self.assertEquals(checkPass(password="123", request=None), True)
        self.assertEquals(checkPass(password="12345678", request=None), True)
        self.assertEquals(checkPass(password="123ABC", request=None), True)
        self.assertEquals(checkPass(password="123abcA", request=None), False)
        self.assertEquals(checkPass(password="123abcd", request=None), True)
        self.assertEquals(checkPass(password="abcdef", request=None), True)
        self.assertEquals(checkPass(password="Aabcdef", request=None), True)

    def tearDown(self) -> None:
        pass
