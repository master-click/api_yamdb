from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group


GROUPS = ['user', 'moderator', 'admin']
MODELS = []
PERMISSONS = []


class Command(BaseCommand):
    help = 'Создает группы пользователей'

    def handle(self, *args, **options):
        for group_name in self.GROUP_SELECTION:
            group, created = Group.objects.get_or_create(
                name=group_name)  # Добавить группу разрешений
