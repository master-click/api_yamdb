import csv
import os

from django.core.management.base import BaseCommand, CommandError
from reviews.models import Category, Comment, Genre, Review, Title, User

import api_yamdb.settings as settings

# команда будет доступна, когда приложение review будет зарегестрировано
# в INSTALLED_APPS
# валидаторы на уровне модели
# последовательность ввода важна
# где ссылка на др модель - важен сам объект
# нужно создать ридми
# не через for а как-то по другому, чтобы не останавливался
# нужно создавать промежуточные таблицы (жанр_произведение)


FILE_TO_MODEL = {
    1: ['category.csv', Category],
    2: ['genre.csv', Genre],
    3: ['users.csv', User],
    4: ['titles.csv', Title],
    5: ['review.csv', Review],
    6: ['comments.csv', Comment],
    # 7: ['genre_title', GEnre_Title]
}

FIELDS = ['author', 'category', 'role']  # fieldsname для добавления '_id'


class Command(BaseCommand):
    help = 'Загружает данные Comments в базу данных'

    def upload_to_db(self, filename, model):
        file_path = os.path.join(
            settings.STATICFILES_DIRS[0], 'data', filename)
        with open(file_path, 'r', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            csv_reader.fieldnames = [
                n + '_id' if n in FIELDS else n for n in csv_reader.fieldnames]
            for row in csv_reader:
                try:
                    _, created = model.objects.get_or_create(**row)
                except Exception as e:
                    raise CommandError(
                        f'Ошибка ввода данных из {filename}: {str(e)}')
                if created == 1:
                    text = f'Добавлены данные: {row}'
                else:
                    text = f'Получены данные: {row}'
                self.stdout.write(self.style.SUCCESS(text))

    def handle(self, *args, **options):
        for i in range(1, len(FILE_TO_MODEL)):
            filename, model = FILE_TO_MODEL.get(i)
            self.upload_to_db(filename, model)


#  сдулать список headers
# первый ряд надо отр
# надо испортировать в базу данных по моделям
# надо проверять данные перед отправкой - сериализаторы помогут??
# как если бы создавали данные? и как чтобы не оставливал работу при ошибке
# -есть там какой-то подход забыл название.
# как распределеить по моделям? вручную?

# нужен специальный сериализатор для каждой модели?
# десериализаторы
