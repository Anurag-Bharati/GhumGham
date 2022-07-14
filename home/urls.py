from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name="home"),
    path('explore/', views.explore, name="explore"),
    path('profile/', views.profile, name="profile"),
    path('statement/', views.statement, name="statement"),
    path('updatep', views.update_profile, name="update-p"),
    path('myorders', views.myBookings, name="get-my-orders"),
    path('packages/<int:identity>', views.packages, name="view-package"),
]
