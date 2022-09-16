from rest_framework import permissions


class AdminOnly(permissions.BasePermission):
    """Права доступа принадлежат администратору."""
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.is_admin
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.is_admin
        )
