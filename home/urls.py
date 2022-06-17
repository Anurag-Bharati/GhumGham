from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name="home"),
    path('explore/', views.explore, name="explore"),
    path('packages/', views.packages, name="packages"),
    path('profile/', views.profile, name="profile"),
    path('statement/', views.statement, name="statement"),
    path('updatep', views.update_profile, name="update-p"),
]
