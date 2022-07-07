from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name="home"),
    path('explore/', views.explore, name="explore"),
    path('profile/', views.profile, name="profile"),
    path('packages/<int:identity>', views.packages, name="view-package"),

]
