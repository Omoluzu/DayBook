#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import datetime
import configparser

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QKeySequence
from pathlib import Path

from modules.TextDay import StartDay
from modules.GuiMenuBar import AppMenuBar
from UI import *

VERSION = "2.1.15"

PATH_CONFIG = os.path.join(Path.home(), "DayBook")
FILE_CONFIG = os.path.join(PATH_CONFIG, "settings.ini")

if os.path.isfile("history.md"):  # Для удобства разработка, чтобы конфигурационный файл был отдельно
    FILE_CONFIG = "settings.ini"


def check_file_config():
    """ Проверка на наличие файла конфигурации и создание его при отсутствие """

    if not os.path.isdir(PATH_CONFIG):
        os.mkdir(PATH_CONFIG)
        print(f"LOG: Была создана папка с файлом конфигурации: {PATH_CONFIG}")

    if not os.path.isfile(FILE_CONFIG):

        config = configparser.ConfigParser()

        config.add_section("OTHER")
        config.set("OTHER", "path_save_daybook", os.path.abspath(os.curdir))  # Путь хранения записей дневника
        config.set("OTHER", "days_of", str(datetime.datetime.now().date()))  # Дата начала ведения дневника
        config.add_section("TEXT")
        config.set("TEXT", "size", str(datetime.datetime.now().date()))  # Размер шрифта

        with open(FILE_CONFIG, "w") as config_file:
            config.write(config_file)
            print(f"LOG: Был создан файл конфигурации: {FILE_CONFIG}")


class AppStart(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(f"DayBook {VERSION}")

        self.config = configparser.ConfigParser()
        self.config.read(FILE_CONFIG)

        self.size_window = QDesktopWidget().screenGeometry()  # Получение разрешение экрана
        self.indent_width = int((self.size_window.width() / 2) - 400)  # Отступ по ширине

        self.setGeometry(self.indent_width, 50, 800, 800)

        self.start_day = StartDay(file_config=FILE_CONFIG, parent=self)
        self.gui_settings = SettingsWidget(parent=self, file_config=FILE_CONFIG)  # Окно настроек
        self.gui_about = AboutWidget(parent=self)  # Окно о программе

        # Горячие клавиши
        self.key_ctrl_s = QShortcut(QKeySequence('Ctrl+S'), self)
        self.key_ctrl_s.activated.connect(self.start_day.save)

        # Виджеты ТабВиджетов
        self.day_book = DayBookWidget(parent=self)
        self.task = TaskBar()

        # ТабВиджет
        self.t_bar = QTabWidget()
        self.t_bar.setTabPosition(QTabWidget.West)
        self.t_bar.addTab(self.day_book, "Дневник")
        self.t_bar.addTab(self.task, "Задачи")

        # Layout
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.t_bar)

        # Widget
        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

        # Menu
        self.menu_bar = AppMenuBar(parent=self)

        self.setMenuBar(self.menu_bar)
        self.show()


if __name__ == "__main__":

    check_file_config()  # Проверяем наличия файла конфигурации.

    app = QApplication([])
    window = AppStart()
    app.exec_()
