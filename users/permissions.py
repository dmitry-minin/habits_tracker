from rest_framework.permissions import BasePermission

from .models import User


class IsOwner(BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        return request.user == obj.user
