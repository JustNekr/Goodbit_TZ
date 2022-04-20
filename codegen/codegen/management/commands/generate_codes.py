import json
import random
import string

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Generate amount codes in group'
    code_length = 6
    # json_file_name = 'codes.json'

    def add_arguments(self, parser):
        parser.add_argument('-amount', required=True, type=int)
        parser.add_argument('-group', required=True)
        parser.add_argument('-file_name', default="codes.json")

    def handle(self, *args, **options):
        # self.stdout.write(f"количество кодов: {options['amount']}\nгруппа: {options['group']}")
        self.json_file_name = options['file_name']
        try:
            with open(self.json_file_name, 'rb+') as f:
                file_string = f.read()
                f.seek(0)
                file_obj = json.loads(f.read())
                if options['group'] in file_obj.keys():
                    last_code = bytes(file_obj[options["group"]][-1], encoding='utf-8')
                    index = file_string.find(last_code) + len(file_obj[options['group']][-1]) + 1
                    f.seek(index)
                    f.write(b', ')
                    for i in range(options['amount']):
                        new_code = bytes(f'"{self.generate_code()}"', encoding='utf-8')
                        f.write(new_code)
                        if i < options['amount'] - 1:
                            f.write(b', ')
                    f.write(file_string[index:])
                else:
                    index = file_string.rfind(b'}')
                    f.seek(index)
                    f.write(bytes(f', "{options["group"]}": [', encoding='utf-8'))
                    for i in range(options['amount']):
                        new_code = bytes(f'"{self.generate_code()}"', encoding='utf-8')
                        f.write(new_code)
                        if i < options['amount'] - 1:
                            f.write(b', ')
                    f.write(b']')
                    f.write(file_string[index:])
        except FileNotFoundError:
            with open(self.json_file_name, 'w') as f:
                new_group = {options['group']: [self.generate_code() for _ in range(options["amount"])]}
                json.dump(new_group, f)

    def generate_code(self):
        while True:
            letters_and_digits = string.ascii_letters + string.digits
            rand_string = ''.join(random.sample(letters_and_digits, self.code_length))
            if self.code_unic_check(rand_string):
                return rand_string
            else:
                continue

    def code_unic_check(self, code):
        try:
            with open(self.json_file_name, 'r') as f:
                if code in f.read():
                    return False
                else:
                    return True
        except FileNotFoundError:
            return True



