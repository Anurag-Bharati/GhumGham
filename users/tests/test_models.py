from django.test import TestCase
from users.models import Customer, Staff
from .test_views import create_user

class TestModels(TestCase):

    customer = Customer()
    staff = Staff()

    @classmethod
    def setUpTestData(cls):

        cls.staff.user = create_user(name="lol1", email="lol1", is_staff=True)
        cls.customer.user = create_user(name="lol2", email="lol2", is_staff=False)
        cls.staff.name = "lol1"
        cls.customer.name = "lol2"

    def test_staff_creation(self):
        self.assertEquals(self.staff.user.is_staff, True)
        self.assertEquals(self.staff.user.is_customer, False)

    def test_customer_creation(self):
        self.assertEquals(self.customer.user.is_customer, True)
        self.assertEquals(self.customer.user.is_staff, False)

    def test_custom_staff_str_method(self):
        self.assertEquals(self.staff.__str__(), "lol1")

    def test_custom_customer_str_method(self):
        self.assertEquals(self.customer.__str__(), "lol2")
