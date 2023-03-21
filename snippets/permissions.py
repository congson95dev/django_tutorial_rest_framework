from rest_framework import permissions


# Allow only the creator of a snippet may update or delete it.
# source: https://www.django-rest-framework.org/tutorial/4-authentication-and-permissions/
class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.owner == request.user


# Allow only admin to create, update, delete records.
class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        # is_staff is considered admin in django
        return bool(request.user and request.user.is_staff)
