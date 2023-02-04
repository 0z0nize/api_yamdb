import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User

FILE_TO_MODELS = [
    ('category.csv', Category),
    #('comments.csv', Comment),
    ('genre.csv', Genre),
    #('genre_title.csv', Title.genre.through),
    #('review.csv', Review),
    ('titles.csv', Title),
    ('users.csv', User),
]


class Command(BaseCommand):

    # def handle(self, *args, **kwargs):

    #     for csv_file, model in FILE_TO_MODELS:
    #         location = os.path.join(settings.CSV_DATA_DIR, csv_file)
    #         fff = pathlib.PurePath(location)
    #         open(location)
    #         self.stdout.write(
    #             f'Модель: {model}; Путь: {location}'
    #         )

    def handle(self, *args, **options):

        if options['clear']:
            for csv_file, model in FILE_TO_MODELS:
                model.objects.all.delete()

        for csv_file, model in FILE_TO_MODELS:
            import_csv_data(
                os.path.join(settings.CSV_DATA_DIR, csv_file), model
            )

    def add_arguments(self, parser):
        parser.add_argument(
            '-c',
            '--clear',
            action='store_true',
            default=False,
            help='Clear model befor import'
        )


def import_csv_data(csv_file, model):
    with open(csv_file, encoding='utf-8') as csv_model_data:
        csv_reader = csv.reader(csv_model_data, delimiter=',')
        fields = next(csv_reader)
        for count, field in enumerate(fields):
            if (model._meta.get_field(field).is_relation and not
                    field.endswith('_id')):
                fields[count] += "_id"

        for row in csv_reader:
            value = {
                field: row[count] for count, field in enumerate(fields)
            }
            _, created = model.objects.get_or_create(**value)
