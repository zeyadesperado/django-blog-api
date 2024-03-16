"""
Serializers for Blog APIS.
"""
from rest_framework import serializers

from user.serializers import UserSerializer

from .models import Post


class PostSerializer(serializers.ModelSerializer):
    """Serializer for Posts"""

    class Meta:
        model = Post
        fields = ['id','title', 'content','created_at', 'updated_at']
        read_only_fields = ['id']


class PostDetailSerializer(PostSerializer):
    """Serializer for detailed Post view"""
    author = UserSerializer()

    class Meta(PostSerializer.Meta):
        fields = PostSerializer.Meta.fields + ['author']
