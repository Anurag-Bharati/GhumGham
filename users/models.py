from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=255, unique=False)
    address = models.CharField(max_length=255, unique=False, blank=True, null=True)
    image = models.ImageField(null=True, blank=True, default="../../static/images/user.png")
    cover_image = models.ImageField(null=True, blank=True, default="../../static/images/pattern.png")
    created_date = models.DateField(auto_now_add=True)

    is_customer = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_ban = models.BooleanField(default=False)

    def __str__(self):
        return self.username.capitalize()

    def is_a_customer(self):
        return self.is_customer
