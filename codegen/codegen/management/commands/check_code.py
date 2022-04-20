import json

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'checking code existing in file and return his group'

    def add_arguments(self, parser):
        parser.add_argument('-code', required=True)
        parser.add_argument('-file_name', default="codes.json")

    def handle(self, *args, **options):
        try:
            with open(options['file_name'], 'r') as f:
                file_obj = json.load(f)
                code_found = None
                for items in file_obj.items():
                    if options['code'] in items[1]:
                        self.stdout.write(f'код существует группа = {items[0]}', ending='')
                        code_found = True
                        break
                if not code_found:
                    self.stdout.write('код не существует', ending='')
        except FileNotFoundError:
            self.stdout.write('файл не найден', ending='')

