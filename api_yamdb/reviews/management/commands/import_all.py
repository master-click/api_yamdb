import csv
import os
from re import A

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from reviews.models import Category, Comment, Genre, Review, Title, TitleGenre

import api_yamdb.settings as settings

User = get_user_model()

FILE_TO_MODEL = {
    1: ['category.csv', Category],
    2: ['genre.csv', Genre],
    3: ['users.csv', User],
    4: ['titles.csv', Title],
    6: ['review.csv', Review],
    7: ['comments.csv', Comment],
    5: ['genre_title.csv', TitleGenre]
}

FIELDS = ['author', 'category']  # fieldsname для добавления '_id'


class Command(BaseCommand):
    help = 'Загружает данные в базу данных'

    def upload_to_db(self, filename, model):
        file_path = os.path.join(
            settings.STATICFILES_DIRS[0], 'data', filename)
        with open(file_path, 'r', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            csv_reader.fieldnames = [
                n + '_id' if n in FIELDS else n for n in csv_reader.fieldnames]
            for row in csv_reader:
                row_id = row.pop('id')
                try:
                    obj = model.objects.get(id=row_id)
                    # через id сделал, почему была проблема для ревью и комментария,
                    # по всем данным, а не только по id при повторном нажатии выходила,
                    # ошибка по тому что нарушена уникальность id
                    self.stdout.write(self.style.SUCCESS(
                        f'данные уже в базе {filename} - {row}'))
                except model.DoesNotExist:
                    row['id'] = row_id
                    try:
                        obj = model(**row)
                        obj.save()
                    except Exception as e:
                        raise CommandError(
                            f'Ошибка ввода данных из {filename}, {row} {str(e)}')
                    self.stdout.write(self.style.SUCCESS(
                        f'добавлены данные {filename} - {row}'))

    def handle(self, *args, **options):
        for i in range(1, len(FILE_TO_MODEL)+1):
            filename, model = FILE_TO_MODEL.get(i)
            self.upload_to_db(filename, model)
