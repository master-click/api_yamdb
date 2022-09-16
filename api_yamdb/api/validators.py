from rest_framework.exceptions import ValidationError
from users.models import User


def validate_username(username):
    """Проверка имени пользователя."""
    if username == 'me':
        raise ValidationError('Недопустимое имя пользователя!')
    elif User.objects.filter(username=username).exists():
        raise ValidationError('Данное имя пользователя уже занято!')


def validate_email(value):
    """Проверка адреса электронной почты."""
    if User.objects.filter(email=value).exists():
        raise ValidationError('Данный адрес электронной '
                              'почты уже используется!')
