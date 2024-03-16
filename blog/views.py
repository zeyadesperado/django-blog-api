"""
Views for the recipe APIs
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import Post
from .serializers import *
from .permissions import IsAuthorOrReadOnly

class PostViewSet(viewsets.ModelViewSet):
    """View for managing Posts"""
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    def get_serializer_class(self):
        """return the serializer class for requests"""
        if self.action == 'list':
            return PostDetailSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new Post with the User as Author."""
        serializer.save(author=self.request.user)
