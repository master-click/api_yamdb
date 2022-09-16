from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied


class IsOwnerAdminModeratorOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    """
    Доступ на чтение - всем, добавление - авторизованным пользователям,
    изменение объектов - авторам этих объектов, модераторам или администраторам
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        user_status = [
            obj.author == request.user,
            request.user.is_staff,
            request.user.groups.filter(name='moderator').exists()
        ]
        if any(user_status):
            return True
        raise PermissionDenied('Изменение чужого контента запрещено!')



