from django.shortcuts import render
from rest_framework import generics

from core.models import User
from core.serializers import UserCreateSerializer


class UserCreateView(generics.CreateAPIView):
    model = User
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()
