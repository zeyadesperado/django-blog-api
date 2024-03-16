"""
Views for the User API.
"""
from rest_framework import generics

from .serializers import UserSerializer


class RegisterUserView(generics.CreateAPIView):
    """Registering a new user in the app"""
    serializer_class = UserSerializer
