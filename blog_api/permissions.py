from rest_framework.permissions import BasePermission, SAFE_METHODS


class PostUserWritePermission(BasePermission):
    """
    Allow only authors of an object to edit it.
    Assumes the model instance has an 'author' attribute.
    """
    message = 'Editing posts is restricted to the author only.'

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user
