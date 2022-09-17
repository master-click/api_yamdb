from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied


class AdminOnly(permissions.BasePermission):
    """Права доступа принадлежат администратору."""
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.is_admin
        )

    def has_object_permission(self, request, view, obj):  # вроде можно убрать про object
        return (
            request.user
            and request.user.is_authenticated
            and request.user.is_admin
        )


class IsAdminOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    """Права на создание и доступа к объекту принадлежат администратору."""
    def has_permission(self, request, view):
        return (
            not request.method == 'POST' or
            (request.user
            and request.user.is_authenticated
            and request.user.is_admin)
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.is_admin
        )


class IsOwnerAdminModeratorOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    """
    Доступ на чтение - всем, добавление - авторизованным пользователям,
    изменение объектов - авторам этих объектов, модераторам или администраторам
    """
    def has_permission(self, request, view):
        return (
            not request.method == 'POST' or
            request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method == 'POST' or
            obj.author == request.user or
            request.user.role != 'user'
        )
