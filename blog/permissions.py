from rest_framework import permissions

class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow authors of a post to edit or delete it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for any user
        if request.method in permissions.SAFE_METHODS:
            return True

        # update and delete  are only allowed to the author of the post
        return obj.author == request.user
