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
from versions import info

PATH_CONFIG = os.path.join(Path.home(), "DayBook")
FILE_CONFIG = os.path.join(PATH_CONFIG, "settings.ini")

if os.path.isfile("history.md"):  # Для удобства разработка, чтобы конфигурационный файл был отдельно
    FILE_CONFIG = "settings.ini"

if sys.platform == "win32":
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(f'home.DayBool.{info["version"]}')


class AppStart(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(f"DayBook {info['version']}")
        self.setWindowIcon(QIcon(":/day_book.png"))

        self.config = configparser.ConfigParser()
        self.config.read(FILE_CONFIG)

        self.size_window = QDesktopWidget().screenGeometry()  # Получение разрешение экрана
        self.indent_width = int((self.size_window.width() / 2) - 400)  # Отступ по ширине

        self.setGeometry(self.indent_width, 50, 800, 800)

        self.start_day = StartDay(file_config=FILE_CONFIG, parent=self)
        self.gui_settings = SettingsWidget(parent=self, file_config=FILE_CONFIG)  # Окно настроек
        self.gui_about = modules.AboutWidget(parent=self)  # Окно о программе

        # Виджеты ТабВиджетов
        self.day_book = modules.DayBook.UI.DayBookWidget(parent=self)
        current_task = modules.CurrentTask.UI.CurrentTaskBar(app=self)
        task = modules.Task.UI.TaskBar(parent=self)

        # ТабВиджет
        self.t_bar = QTabWidget()
        self.t_bar.setTabPosition(QTabWidget.West)
        self.t_bar.addTab(self.day_book, "Дневник")
        self.t_bar.addTab(current_task, "Текущая задача")
        self.t_bar.addTab(task, "Список задачи")

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

        # Горячие клавиши
        self.key_ctrl_s = QShortcut(QKeySequence('Ctrl+S'), self)
        self.key_ctrl_s.activated.connect(self.start_day.save)

        self.key_ctrl_t = QShortcut(QKeySequence('Ctrl+T'), self)
        self.key_ctrl_t.activated.connect(self.day_book.insert_current_time)


if __name__ == "__main__":

    config = Config()
    config.check_config()
    config.check_parameters()
    del config

    app = QApplication([])
    window = AppStart()
    app.exec_()
