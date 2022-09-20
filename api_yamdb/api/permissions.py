from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Права на создание и доступа к объекту принадлежат администратору.
    Category, Genre, Title
    """
    def has_permission(self, request, view):
        return (
            not request.method == 'POST'
            or (request.user
                and request.user.is_authenticated
                and request.user.is_admin))

    def has_object_permission(self, request, view, obj):
        return ((
            request.user
            and request.user.is_authenticated
            and request.user.is_admin
        ) or request.method == 'GET')


class IsOwnerAdminModeratorOrReadOnly(permissions.BasePermission):
    """
    Доступ на чтение - всем, добавление - авторизованным пользователям,
    изменение объектов - авторам этих объектов, модераторам или администраторам
    """
    def has_permission(self, request, view):
        return (
            not request.method == 'POST'
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method == 'GET'
            or (request.user.is_authenticated
                and (obj.author == request.user
                     or request.user.role != 'user'
                     or request.user.is_admin))
        )
