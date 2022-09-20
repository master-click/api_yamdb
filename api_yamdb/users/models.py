from django.db import models
from django.contrib.auth.models import AbstractUser

from django.db import models

from .validators import validate_username


class User(AbstractUser):
    """Добавление дополнительных полей."""
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'

    ROLE = (
        (ADMIN, 'Администратор'),
        (USER, 'Аутентифицированный пользователь'),
        (MODERATOR, 'Модератор'),
    )
    role = models.CharField('Роль',
                            max_length=35,
                            choices=ROLE,
                            default=USER
                            )
    email = models.EmailField(unique=True)
    bio = models.TextField('Краткая информация',
                           blank=True,
                           max_length=255
                           )
    username = models.CharField(max_length=30, unique=True,
                                validators=[validate_username])

    class Meta:
        ordering = ('role',)
        verbose_name = 'Пользователи'

    @property
    def is_admin(self):
        return self.is_superuser or self.role == self.ADMIN

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_user(self):
        return self.role == self.USER
