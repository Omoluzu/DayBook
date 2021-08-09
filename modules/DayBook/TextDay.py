#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import datetime
import configparser
from pathlib import Path


PATH_CONFIG = os.path.join(Path.home(), "DayBook")
FILE_CONFIG = os.path.join(PATH_CONFIG, "settings.ini")

DICT_MONTH = {
    1: {
        "save": "01.Январь",
        "welcome": "Января"
    },
    2: {
        "save": "02.Февраль",
        "welcome": "Февраля"
    },
    3: {
        "save": "03.Март",
        "welcome": "Марта"
    },
    4: {
        "save": "04.Апрель",
        "welcome": "Апреля"
    },
    5: {
        "save": "05.Май",
        "welcome": "Мая"
    },
    6: {
        "save": "06.Июнь",
        "welcome": "Июня"
    },
    7: {
        "save": "07.Июль",
        "welcome": "Июля"
    },
    8: {
        "save": "08.Август",
        "welcome": "Августа"
    },
    9: {
        "save": "09.Сентябрь",
        "welcome": "Сентября"
    },
    10: {
        "save": "10.Октябрь",
        "welcome": "Октября"
    },
    11: {
        "save": "11.Ноябрь",
        "welcome": "Ноября"
    },
    12: {
        "save": "12.Декабрь",
        "welcome": "Декабря"
    },
}

DICT_WEEKDAY = {
    0: "Понедельник",
    1: "Вторник",
    2: "Среда",
    3: "Четверг",
    4: "Пятница",
    5: "Суббота",
    6: "Воскресенье",
}


class StartDay:
    """
    Возвращает или создает запись текущего дня
    """
    def __init__(self, parent):
        self.file_config = FILE_CONFIG
        self.parent = parent

        self.check_read = False  # Чек на возможность введения записей в дневнике

        self.config = configparser.ConfigParser()  # Загружаем файл конфигурации
        self.config.read(self.file_config)  # Считываем файл конфигурации

        self.current_date = datetime.datetime.now()  # Текущее дата

        self.path_daybook = self.get_path_save()  # Получение полного пути сохраняемого файла
        self.name_file_day = f"day_{self.current_date.strftime('%Y-%m-%d')}.txt"
        self.path_day = os.path.join(self.path_daybook, self.name_file_day)

    def get_path_save(self):
        """ Получение полного пути сохраняемого файла """
        path_daybook = self.config.get("OTHER", "path_save_daybook")
        if os.path.exists(path_daybook):
            path_year = os.path.join(path_daybook, str(self.current_date.year))
            self.check_folder(path_year)
            path_month = os.path.join(path_year, DICT_MONTH[self.current_date.month]['save'])
            self.check_folder(path_month)
            return path_month
        else:
            self.check_read = "Директории хранения файлов не существует. Проверьте пожалуйста настойки"
            print("LOG: Дирректории хранения файлов не существует.")
            return path_daybook

    @staticmethod
    def check_folder(folder):
        """ Проверка наличие папки и её создание """
        if not os.path.isdir(folder):
            os.mkdir(folder)
            print(f"LOG: Созданна папка: {folder}")

    def start(self):
        """ Открытие или создание новой записей дневника  """

        if os.path.isfile(self.path_day):
            with open(self.path_day, "r", encoding="utf-8") as file:
                return file.read()
        else:
            return self.welcome_entry()

    def welcome_entry(self):
        """ Приветственая запись при создании нового дня """
        if self.check_read:
            return self.check_read
        else:
            day = str(self.current_date.day)
            month = DICT_MONTH[self.current_date.month]['welcome']
            year = str(self.current_date.year)
            weekday = DICT_WEEKDAY[self.current_date.weekday()]
            days_of = datetime.datetime.now() - datetime.datetime.strptime(self.config.get("OTHER", "days_of"), "%Y-%m-%d")
            return f"{day} {month} {year} - ({weekday}) - Дней ведения дневника: {days_of.days}"

    def save(self):
        """ Сохранение записей дневника """
        if not self.check_read:
            with open(self.path_day, "w", encoding="utf-8") as text:
                text.write(self.parent.toPlainText())
