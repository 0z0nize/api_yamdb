import csv
import os
import sys

from colorama import Fore
from django.conf import settings
from django.core.management.base import BaseCommand
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User

FILE_TO_MODELS = [
    ('users.csv', User),
    ('category.csv', Category),
    ('titles.csv', Title),
    ('genre.csv', Genre),
    ('genre_title.csv', Title.genre.through),
    ('review.csv', Review),
    ('comments.csv', Comment),
]


class Command(BaseCommand):
    help = 'Upload data from csv file to sql database'

    def handle(self, **options):

        if options['clear']:
            for csv_file, model in FILE_TO_MODELS:
                model.objects.all().delete()

        for csv_file, model in FILE_TO_MODELS:
            import_csv_data(
                self,
                os.path.join(settings.CSV_DATA_DIR, csv_file),
                model
            )

    def add_arguments(self, parser):
        parser.add_argument(
            '-c',
            '--clear',
            action='store_true',
            default=False,
            help='Clear before import'
        )


def import_csv_data(self, csv_file, model):
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
            if not created:
                sys.exit(
                    Fore.LIGHTYELLOW_EX + '\nCSV to database record - ERORR!!!'
                    + Fore.RED + '\n\nIncorrect data:'
                    + Fore.BLUE + f'\n{value}\n\n'
                    + Fore.LIGHTMAGENTA_EX
                    + '!!!Clear database before recording.!!!\n'
                )
            self.stdout.write(
                Fore.WHITE + 'Recorded: ' + Fore.GREEN + f'{created}'
                + Fore.LIGHTBLACK_EX + f'\n{value}\n\n'
            )
