from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import SimpleRouter

from core.views import UserCreateView, UserLoginView, ProfileView, UpdatePasswordView

urlpatterns = [
    path('signup', UserCreateView.as_view(), name='signup'),
    path('login', UserLoginView.as_view(), name='login'),
    path('profile', ProfileView.as_view(), name='user'),
    path('update_password', UpdatePasswordView.as_view(), name='update_password'),
]
