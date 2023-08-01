import argparse


class Parser:
    def __init__(self):
        self._parser = argparse.ArgumentParser(description='Параметры для работы')
        self._standard_args_group = self._parser.add_argument_group('Основные аргументы')
        self._specific_args_group = self._parser.add_argument_group('Дополнительные аргументы')

        self._standard_args_group.add_argument('-c', '--config',
                                               required=True,
                                               action='store',
                                               help='Путь к конфиг файлу')

        self._standard_args_group.add_argument('-e', '--edit',
                                               required=False,
                                               action='store_true',
                                               help='Создать или отредактировать конфиг файл.')

    def get_args(self):
        """
        Возвращает аргументы командной строки для подключения к vSphere.
        """
        return self._parser.parse_args()

    def add_custom_argument(self, *name_or_flags, **options):
        """
        Uses ArgumentParser.add_argument() to add a full definition of a command line argument
        to the "sample specific arguments" group.
        https://docs.python.org/3/library/argparse.html#the-add-argument-method
        """
        self._specific_args_group.add_argument(*name_or_flags, **options)
