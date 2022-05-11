from django.test import SimpleTestCase

from users.forms import *


class TestForms(SimpleTestCase):

    def test_login_form_valid_invalid_data(self):
        valid_form = LoginForm(data={
            'username': 'test',
            'password': 'test',

        })
        invalid_form = LoginForm(data={
            'username': 'test',
        })
        self.assertTrue(valid_form.is_valid())
        self.assertFalse(invalid_form.is_valid())
        self.assertEquals(len(invalid_form.errors), 1)

    def test_register_form_valid_invalid_data(self):
        valid_form = RegistrationForm(data={
            'username': 'test',
            'email': 'test@test.com',
            'password': 'test',
        })
        invalid_form = RegistrationForm(data={
            'username': 'test',
        })
        self.assertTrue(valid_form.is_valid())
        self.assertFalse(invalid_form.is_valid())
        self.assertEquals(len(invalid_form.errors), 2)
