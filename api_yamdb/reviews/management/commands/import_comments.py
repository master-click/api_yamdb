import csv
import os
from django.apps import apps
import api_yamdb.settings as settings
from django.core.management.base import BaseCommand, CommandError
from review.models import Review, Comment, User, Title, Genre, Category

# команда будет доступна, когда приложение review будет зарегестрировано в INSTALLED_APPS
# валидаторы на уровне моели
# последовательность ввода важна
# где ссылка на др модель - важен сам объект
#  нужно создать ридми
# не через for а как-то по другому, чтобы не останавливался


def add_reviews(self):
    file_path = os.join.path(settings.STATICFILES_DIRS, 'data', 'review.csv')
    with open(file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            try:
                Comment.objects.get_or_create(
                    id=row[0],
                    title=row[1],
                    text=row[2],
                    author=row[3],
                    score=row[4],
                    pub_date=row[5])
                    # вроде можно универсальную через список, но названия полей не совпадают
            except Exception as e:  # кажется можно лучше сделать
                raise CommandError(
                    f'Ошибка ввода данных в {Comment}: {str(e)}')
            self.stdout.write(self.style.SUCCESS(
                f'Успешно добавлены данные комментария: {row[0]} (id)'))


def add_titles(self):
    file_path = os.join.path(settings.STATICFILES_DIRS, 'data', 'titles.csv')
    with open(file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            try:
                Comment.objects.get_or_create(
                    id=row[0],
                    name=row[1],
                    year=row[2],
                    category=row[3])
                    # вроде можно универсальную через список, но названия полей не совпадают
            except Exception as e:  # кажется можно лучше сделать
                raise CommandError(
                    f'Ошибка ввода данных в {Comment}: {str(e)}')
            self.stdout.write(self.style.SUCCESS(
                f'Успешно добавлены данные комментария: {row[0]} (id)'))


# можно использовать get_field('name')
# можно сделать форму.

class Command(BaseCommand):
    help = 'Загружает данные Comments в базу данных'
    def handle(self, *args, **options):
        file_path = os.join.path(settings.STATICFILES_DIRS, 'data', 'comments.csv')
        with open(file_path, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            headers = next(reader, None)
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




# ghhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh


#  for field, expected_value in help_texts.items():
#            with self.subTest(field=field):
#                self.assertEqual(
#                    post._meta.get_field(field).help_text, expected_value)


#  можно сделать словарь
#  сдулать список headers
# первый ряд надо отр
# надо испортировать в базу данных по моделям
# надо проверять данные перед отправкой - сериализаторы помогут??
# как если бы создавали данные? и как чтобы не оставливал работу при ошибке
# -есть там какой-то подход забыл название.
# как распределеить по моделям? вручную?

# нужен специальный сериализатор для каждой модели?
# десериализаторы
