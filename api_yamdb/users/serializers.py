from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404

from rest_framework.exceptions import ValidationError

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        password = self.initial_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role', 'password')
        required_fields = ('username', 'password')
        write_only_fields = ('password',)

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response.pop("password", None)
        return response


class UserSerializer(serializers.ModelSerializer):
    posts = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'posts')


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

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name',
                  'last_name', 'bio', 'role')


class SignUpSerializer(serializers.ModelSerializer):
    """Сериализатор процедуры регистрации"""

    class Meta:
        model = User
        fields = ('email', 'username')
