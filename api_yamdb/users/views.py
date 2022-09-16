from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from posts.models import User

from .permissions import IsOwnerOfObject
from .serializers import UserRegistrationSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        """
        Снимает ограничения для создания пользователя
        """
        if self.request.method == 'POST':
            self.permission_classes = [AllowAny]
        elif self.request.method == 'GET':
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [IsOwnerOfObject]
        return super(UserViewSet, self).get_permissions()

    def get_serializer_class(self):
        """
        Задает разные сериализаторы для создания, изменения пользователя
        и других действий
        """
        if self.action == ('create' or 'update'):
            return UserRegistrationSerializer
        return UserSerializer

    # в базовом методе get_permissions
    # есть загадочная строчка кода:
    #         [permission() for permission in permission_classes]
    # получается генерится список, но что делает permission()?
