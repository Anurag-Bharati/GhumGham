from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name="home"),
    path('explore/', views.explore, name="explore"),
    path('packages/', views.packages, name="packages"),
]
