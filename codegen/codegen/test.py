import json
import os
from io import StringIO

from django.core.management import call_command
from django.test import TestCase


class GenerateCodeTestCase(TestCase):
    file_name = 'generate_code_test.json'
    command = 'generate_codes'

    def tearDown(self) -> None:
        super(GenerateCodeTestCase, self).tearDown()
        os.remove(self.file_name)

    def test_mycommand(self):
        """ Test my custom command."""

        opts = {'amount': 2,
                'group': 'fghjk',
                'file_name': self.file_name}
        call_command(self.command, **opts)

        with open(self.file_name, 'r') as f:
            file_obj = json.load(f)
            self.assertEqual(len(file_obj), 1, 'incorrect amount of groups')

    def test_from_tz(self):
        """test from TZ"""
        options_list = [
            {"amount": 10, "group": 'агенства'},
            {"amount": 1, "group": 'агенства'},
            {'amount': 42, 'group': 'avtostop'},
            {'amount': 5, 'group': 1}
        ]

        for options in options_list:
            call_command(self.command, **options, file_name=self.file_name)

        with open(self.file_name, 'r') as f:
            file_obj = json.load(f)

            self.assertEqual(len(file_obj), 3, 'incorrect amount of groups')

            values_list = []
            for value in file_obj.values():
                values_list += value

            self.assertEqual(len(values_list), 58, 'incorrect amount of codes')


class CodeCheckTestCase(TestCase):
    file_name = 'code_check_test.json'
    testing_dict = {
        122: ["ruFATD", "DlwpH5", "0hwQ4S", "uBWOiv"],
        "впвпвпв": ["75grmX", "hZ73Eu", "FAUu9f", "goGzPW"],
        "азимути": ["FXR5kh", "Kepaoj"]
    }
    incorrect_code = 'incorrect_code'
    command = 'check_code'

    def call_command(self, *args, **kwargs):
        out = StringIO()
        call_command(
            self.command,
            *args,
            stdout=out,
            stderr=StringIO(),
            **kwargs,
        )
        return out.getvalue()

    def setUp(self) -> None:
        super(CodeCheckTestCase, self).setUp()
        with open(self.file_name, 'w') as f:
            json.dump(self.testing_dict, f)

    def tearDown(self) -> None:
        super(CodeCheckTestCase, self).tearDown()
        os.remove(self.file_name)

    def test_existed_codes(self):
        for key, values in self.testing_dict.items():
            for value in values:
                out = self.call_command(code=value, file_name=self.file_name)
                self.assertEqual(out, f'код существует группа = {key}', f'код {value} не найден в файле')

    def test_incorrect_code(self):
        out = self.call_command(code=self.incorrect_code, file_name=self.file_name)
        self.assertEqual(out, 'код не существует', f'неверный вывод: {out}')

    def test_incorrect_file(self):
        out = self.call_command(code=self.testing_dict[122][0], file_name='incorrect.json')
        self.assertEqual(out, 'файл не найден', f'обнаружен несуществующий файл ?!?')

