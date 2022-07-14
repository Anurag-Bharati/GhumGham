from django.urls import path
from . import views

urlpatterns = [
    path('', views.authenticate, name="auth"),
    path('activate/<identity>/<token>', views.verification, name="activate"),
    path('activate/', views.activated, name="activated"),
    path('otp/', views.otp_login, name="otp-login"),
    path('recovery/', views.forget_pass, name="forget-pass"),
    path('logout/', views.logout, name="logout")
]
