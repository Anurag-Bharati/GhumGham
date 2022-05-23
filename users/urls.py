from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('activate/<identity>/<token>', views.verification, name="activate"),
    path('activate/', views.activated, name="activated"),
    path('auth/', views.authenticate, name="auth"),
    path('otp/', views.otp_login, name="otp-login")
]
