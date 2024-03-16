"""
Serializers for the user API View.
"""
from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object"""

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'name']
        extra_kwargs = {'password': {'write_only':True, 'min_length': 5}}

    def create(self, validated_data):
        """Create and return a user with encrypted password."""
        email = validated_data.get('email')
        if get_user_model().objects.filter(email=email).exists():
            raise ValidationError("User with this email already exists.")
        return get_user_model().objects.create_user(**validated_data)
