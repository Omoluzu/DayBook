#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import ctypes
import configparser
from ico import recource

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QKeySequence, QIcon
from pathlib import Path

from UI import *
from modules.TextDay import StartDay
from modules.GuiMenuBar import AppMenuBar
from modules.Configuration import Config

import modules

VERSION = "2.2.11"

PATH_CONFIG = os.path.join(Path.home(), "DayBook")
FILE_CONFIG = os.path.join(PATH_CONFIG, "settings.ini")

if os.path.isfile("history.md"):  # Для удобства разработка, чтобы конфигурационный файл был отдельно
    FILE_CONFIG = "settings.ini"

if sys.platform == "win32":
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(f'home.DayBool.{VERSION}')


class AppStart(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(f"DayBook {VERSION}")
        self.setWindowIcon(QIcon(":/day_book.png"))

        self.config = configparser.ConfigParser()
        self.config.read(FILE_CONFIG)

        self.size_window = QDesktopWidget().screenGeometry()  # Получение разрешение экрана
        self.indent_width = int((self.size_window.width() / 2) - 400)  # Отступ по ширине

        self.setGeometry(self.indent_width, 50, 800, 800)

        self.start_day = StartDay(file_config=FILE_CONFIG, parent=self)
        self.gui_settings = SettingsWidget(parent=self, file_config=FILE_CONFIG)  # Окно настроек
        self.gui_about = modules.AboutWidget(parent=self)  # Окно о программе

        # Горячие клавиши
        self.key_ctrl_s = QShortcut(QKeySequence('Ctrl+S'), self)
        self.key_ctrl_s.activated.connect(self.start_day.save)

        # Виджеты ТабВиджетов
        self.day_book = modules.DayBook.UI.DayBookWidget(parent=self)
        task = modules.Task.UI.TaskBar()
        random_task = modules.RandomTask.UI.RandomTaskWidget()

        # ТабВиджет
        self.t_bar = QTabWidget()
        self.t_bar.setTabPosition(QTabWidget.West)
        self.t_bar.addTab(self.day_book, "Дневник")
        self.t_bar.addTab(task, "Задачи")
        self.t_bar.addTab(random_task, "Рандомная задача")

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
        self.showMaximized()


if __name__ == "__main__":

    config = Config()
    config.check_config()
    config.check_parameters()
    del config

    app = QApplication([])
    window = AppStart()
    app.exec_()
