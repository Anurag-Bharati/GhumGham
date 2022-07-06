from django.db import models
from users.models import User


# Create your models here.
class Statement(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now=True)
    # TODO Package, Book ID, Staff Assigned etc
