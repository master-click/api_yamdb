from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from users.models import User
from .validators import validate_username, validate_email


class TokenSerializer(serializers.ModelSerializer):
    """Сериализатор получения токена"""
    confirmation_code = serializers.CharField(allow_blank=False)
    username = serializers.CharField(max_length=64, allow_blank=False)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')

    def validate(self, data):
        user = get_object_or_404(User, username=data['username'])
        confirmation_code = default_token_generator.make_token(user)
        if str(confirmation_code) != data['confirmation_code']:
            raise ValidationError('Неверный код подтверждения!')
        return data


class CustomUserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователей"""
    email = serializers.EmailField(max_length=64, allow_blank=False,
                                   validators=[validate_email])
    username = serializers.CharField(max_length=64, allow_blank=False,
                                     validators=[validate_username])

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name',
                  'last_name', 'bio', 'role')


class SignUpSerializer(serializers.ModelSerializer):
    """Сериализатор процедуры регистрации"""
    email = serializers.EmailField(max_length=64, allow_blank=False,
                                   validators=[validate_email])
    username = serializers.CharField(max_length=64, allow_blank=False,
                                     validators=[validate_username])

    class Meta:
        model = User
        fields = ('email', 'username')
