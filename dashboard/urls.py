from django.urls import path
from . import views

urlpatterns = [
    path('', views.Dashboard.as_view(), name="dashboard"),
    path('delete-log/<int:identity>', views.delete_log, name="delete-log"),
    path('ban-user/<int:identity>', views.ban_unban_user, name="ban-unban-user"),
]
