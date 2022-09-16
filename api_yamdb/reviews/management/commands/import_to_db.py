import csv
import os
from django.apps import apps
import api_yamdb.settings as settings
from django.core.management.base import BaseCommand, CommandError
from review.models import Review, Comment, User, Title, Genre, Category

# команда будет доступна, когда приложение review будет зарегестрировано в INSTALLED_APPS

# можно сделать словарь для всех
FILES = {'comments.csv': {0: 'id',
                          1: 'review',
                          }
                                   ,
         'category.csv': ,
         'titles.csv': ,


}


class Command(BaseCommand):
    help = 'Загружает данные Comments в базу данных'

    def handle(self, *args, **options):
        file_path = os.join.path(settings.STATICFILES_DIRS, 'data', 'comments.csv')
        with open(file_path, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                try:
                    Comment.objects.get_or_create(
                        id=row[0],
                        review=row[1],
                        text=row[2],
                        author=row[3],
                        pub_date=row[4])
                    # вроде можно универсальную через список, но названия полей не совпадают
                except Exception as e:  # кажется можно лучше сделать
                    raise CommandError(
                        f'Ошибка ввода данных в {Comment}: {str(e)}')
                self.stdout.write(self.style.SUCCESS(
                    f'Успешно добавлены данные комментария: {row[0]} (id)'))



#  можно сделать словарь
#  сдулать список headers

# надо испортировать в базу данных по моделям
# надо проверять данные перед отправкой - сериализаторы помогут??
# как если бы создавали данные? и как чтобы не оставливал работу при ошибке
# -есть там какой-то подход забыл название.
# как распределеить по моделям? вручную?

# нужен специальный сериализатор для каждой модели?
# десериализаторы
