from django.test import TestCase
from users.utils import activation_token as Token
from .test_views import create_user
from django.test import Client

class TestUtils(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.user = create_user(name="test_token", email="test_token_email", is_active=False)

    def setUp(self):
        self.token = Token.make_token(self.user)

    def test_token_is_generated(self):
        self.assertIsNotNone(self.token)

    def test_token_match(self):
        self.assertTrue(Token.check_token(user=self.user, token=self.token))

    def tearDown(self) -> None:
        pass
