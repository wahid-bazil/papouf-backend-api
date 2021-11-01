"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path ,include
from .views import *


urlpatterns = [
    path('registration-Settings', RegistrationSettings.as_view()),
    path('details', UserDetail.as_view()),
    path('contact-details',UserContactDetail.as_view()),
    path('numbers',UserNumbers.as_view()),
    path('sign-up/', CustomUserCreate.as_view()),
    path('email-verify/', VerifyEmail.as_view(),name='email-verify'),
    path('log-in/', LoginAPIView.as_view(), name="login"),
    path('request-reset-email/', RequestPasswordResetEmail.as_view(),
         name="request-reset-email"),
    path('password-reset/<uidb64>/<token>/',
         PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    path('password-reset-complete/', SetNewPasswordAPIView.as_view(),
         name='password-reset-complete'),
    path('is_first_load', FirstLoadView.as_view()),
    
]
