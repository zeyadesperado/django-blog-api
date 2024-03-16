"""
Views for the User API.
"""
from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken

from .serializers import UserSerializer, AuthTokenSerializer


class RegisterUserView(generics.CreateAPIView):
    """Registering a new user in the app"""
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user."""
    serializer_class = AuthTokenSerializer
