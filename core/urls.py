from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import SimpleRouter

from core.views import UserCreateView

urlpatterns = [
    path('signup', UserCreateView.as_view(), name='signup')
]
