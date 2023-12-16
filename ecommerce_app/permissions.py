from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)
    

class ReviewOwnerOrAdminOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Allow admin users to perform any action
        if request.user.is_staff or request.user.is_superuser:
            return True
        elif request.method in permissions.SAFE_METHODS:
            return True
            
         # Allow review owner to perform actions on their own review
        return obj.customer.user == request.user