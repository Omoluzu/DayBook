#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import datetime
import configparser

from PyQt5.QtWidgets import QMainWindow, QShortcut, QTextEdit, QVBoxLayout, QWidget, QApplication, QDesktopWidget
from PyQt5.QtGui import QKeySequence, QFont
from pathlib import Path

from modules.TextDay import StartDay
from modules.GuiSettings import AppGuiSettings, AppGuiAbout
from modules.GuiMenuBar import AppMenuBar

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

        self.config = configparser.ConfigParser()
        self.config.read(FILE_CONFIG)

        self.size_window = QDesktopWidget().screenGeometry()  # Получение разрешение экрана
        self.indent_width = int((self.size_window.width() / 2) - 400)  # Отступ по ширине

        self.setGeometry(self.indent_width, 50, 800, 800)

        self.start_day = StartDay(file_config=FILE_CONFIG, parent=self)
        self.gui_settings = AppGuiSettings(parent=self, file_config=FILE_CONFIG)  # Окно настроек
        self.gui_about = AppGuiAbout(parent=self)  # Окно о программе

        # Горячие клавиши
        self.key_ctrl_s = QShortcut(QKeySequence('Ctrl+S'), self)
        self.key_ctrl_s.activated.connect(self.start_day.save)

        self.font = QFont()
        self.font.setPointSize(self.config.getint("TEXT", "size"))

        # Основная запись дневника
        self.text = QTextEdit()
        self.text.setHtml(self.start_day.start())
        self.text.setReadOnly(True) if self.start_day.check_read else self.text.setReadOnly(False)
        self.text.setFont(self.font)

        # Layout
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.text)

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
