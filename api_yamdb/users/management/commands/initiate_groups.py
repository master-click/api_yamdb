from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group, Permission


GROUPS = ['user', 'moderator', 'admin']
MODELS = []
PERMISSONS = []

class Command(BaseCommand):
    help = 'Создает группы пользователей'


    def handle(self, *args, **options):
        for group_name in self.GROUP_SELECTION:
            group, created = Group.objects.get_or_create(name = group_name) # Добавить группу разрешений




try:
                    model.objects.get_or_create(**row)
                except Exception as e:
                    raise CommandError(
                        f'Ошибка ввода данных из {filename}: {str(e)}')
                self.stdout.write(self.style.SUCCESS(
                    f'Успешно добавлены данные: {row.keys[0]} (id)'))