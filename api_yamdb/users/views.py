from django.conf import settings
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail

from rest_framework import viewsets, filters, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User

from .permissions import AdminOnly, IsOwnerOfObject
from .serializers import (UserRegistrationSerializer, UserSerializer,
                          CustomUserSerializer, SignUpSerializer,
                          TokenSerializer)


class UsersViewSet(viewsets.ModelViewSet):
    """API для работы пользователей."""
    queryset = User.objects.all()
    lookup_field = 'username'
    serializer_class = CustomUserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    pagination_class = PageNumberPagination
    permission_classes = (AdminOnly,)

    @action(detail=False, methods=['get', 'patch'],
            permission_classes=(IsAuthenticated,))
    def me(self, request):
        user = get_object_or_404(User, username=self.request.user.username)
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = self.get_serializer(user,
                                         data=request.data, partial=True)
        if serializer.is_valid():
            if 'role' in request.data:
                if user.role != 'user':
                    serializer.save()
            else:
                serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    if not User.objects.filter(username=request.data['username'],
                               email=request.data['email']).exists():
        serializer.save()
    user = User.objects.get(username=request.data['username'],
                            email=request.data['email'])
    conformation_code = default_token_generator.make_token(user)
    send_mail(f'Доброго дня, {str(user.username)}! Ваш код доступен ниже',
              conformation_code,
              settings.EMAIL_FOR_AUTH_LETTERS,
              [request.data['email']],
              fail_silently=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(User, username=request.data['username'])
    confirmation_code = request.data['confirmation_code']
    if default_token_generator.check_token(
            user=user,
            token=confirmation_code
    ):
        user.is_active = True
        user.save()

        def get_tokens_for_user(current_user):
            refresh = RefreshToken.for_user(current_user)

            return {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }

        result = get_tokens_for_user(user)
    return Response(result)


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
