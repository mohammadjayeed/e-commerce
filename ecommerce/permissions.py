from rest_framework.permissions import BasePermission

class IsAnonymousUser(BasePermission):
    """
    Custom permission class to allow access only to anonymous users.
    """

    def has_permission(self, request, view):
        return request.user.is_anonymous