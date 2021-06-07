#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль для управления конфигурационным файлом
"""

import os
import configparser

from pathlib import Path

from modules.settings import MAIN

PATH_CONFIG = os.path.join(Path.home(), "DayBook")
FILE_CONFIG = os.path.join(PATH_CONFIG, "settings.ini")

if os.path.isfile("history.md"):  # Для удобства разработка, чтобы конфигурационный файл был отдельно
    PATH_CONFIG = os.path.abspath(os.curdir)
    FILE_CONFIG = "settings.ini"


class Config:
    """ Управление конфигурацией программы """
    check_file_config: bool  # Наличие файла конфига

    def __new__(cls, *args, **kwargs):  # Создание singleton класса
        if not hasattr(cls, 'instance'):
            cls.instance = super(Config, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.path_config = PATH_CONFIG  # Путь до места хранения конфигураций
        self.file_config = os.path.join(self.path_config, FILE_CONFIG)  # Путь до файла конфигурации

        self.config = configparser.ConfigParser()
        self.config.read(self.file_config)

        self.check_file_config = True if os.path.exists(self.file_config) else False

    def check_config(self):
        """ Проверка и создание необходимых папок и файлов для работы файла конфигурации """

        if not os.path.isdir(self.path_config):
            os.mkdir(self.path_config)

        if not os.path.isfile(self.file_config):
            with open(self.file_config, "w") as config_file:
                config_file.write("")

    def check_parameters(self):
        """ Проверка на наличие всех параметров и создание их при отсутствии"""

        for section, value in MAIN.items():
            if not self.config.has_section(section):
                self.config.add_section(section)

            for item, key in value.items():
                if not self.config.has_option(section, item):
                    self.config.set(section, item, str(key))

        with open(self.file_config, "w") as config_file:
            self.config.write(config_file)

        self.config.read(self.file_config)

    def update(self, selection, option, value):
        """ Обновление файла конфигурации """
        self.config.set(selection, option, str(value))

        with open(self.file_config, "w") as config_file:
            self.config.write(config_file)

    def get(self, selection: str, option: str, array: bool = False):
        """
        Получение параметра конфигурации

        selection: str = Секция
        option: str = Наименование параметра
        array: bool = При установки флага возвращаемый элемент вернет как массив.
        """
        if self.check_file_config:
            try:
                if array:
                    return [x for x in self.config.get(selection, option).split(";")]
                else:
                    return self.config.get(selection, option)

            except configparser.NoOptionError:
                print(f"configparser.NoOptionError: Нет такого параметра в файле конфигов: {selection} - {option}")
                return False
            except configparser.NoSectionError:
                print(f"configparser.NoOptionError: Нет такой секции в файле конфигов: {selection}")
                return False
        else:
            return False
