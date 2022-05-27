from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=255, unique=False)
    address = models.CharField(max_length=255, unique=False, null=True)

    is_customer = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    def is_a_customer(self):
        return self.is_customer

class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=120, unique=True)
    address = models.CharField(max_length=220)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=120, unique=True)
    address = models.CharField(max_length=220)
    image = models.ImageField(null=True, default="../default_customer.png")
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name
