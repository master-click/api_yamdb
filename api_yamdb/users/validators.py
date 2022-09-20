from rest_framework.exceptions import ValidationError


def validate_username(username):
    """Проверка имени пользователя."""
    if username == 'me':
        raise ValidationError('Недопустимое имя пользователя!')
