from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'is_customer', 'is_staff', 'is_admin', 'is_superuser']


admin.site.register(User, UserAdmin)
