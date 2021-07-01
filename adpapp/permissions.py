
from rest_framework.permissions import BasePermission

class IsOwnerOrSuperuser(BasePermission):
    """
    Checks if an authenticated user is matches a 
    profile or if the user is a superadmin
    """

    def has_object_permission(self, request, view, obj):
        return request.user.id == obj.id or request.user.is_superuser