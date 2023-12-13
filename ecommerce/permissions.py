from rest_framework import permissions

class IsAnonymousUser(permissions.BasePermission):
    """
    Custom permission class to allow access only to anonymous users.
    """

    def has_permission(self, request, view):
        return request.user.is_anonymous
    
