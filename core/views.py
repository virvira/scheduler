from typing import Any

from django.contrib.auth import login, logout
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import generics
from rest_framework.generics import RetrieveUpdateDestroyAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from core.models import User
from core.serializers import UserCreateSerializer, UserLoginSerializer, ProfileSerializer


class UserCreateView(generics.CreateAPIView):
    model = User
    serializer_class = UserCreateSerializer


class UserLoginView(generics.CreateAPIView):
    model = User
    serializer_class = UserLoginSerializer

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        login(request=request, user=serializer.save())
        return Response(serializer.data)


class ProfileView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def perform_destroy(self, instance):
        logout(self.request)


class UpdatePasswordView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = User
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user
