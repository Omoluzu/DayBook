#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import ctypes
import argparse
# import configparser
from ico import recource

from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QTabWidget, QHBoxLayout, QWidget, QShortcut, QApplication
from PyQt5.QtGui import QKeySequence, QIcon
from pathlib import Path

from UI import *
from modules.GuiMenuBar import AppMenuBar
from modules.Configuration import Config

import modules
from versions import info

parser = argparse.ArgumentParser(description="DayBook")
parser.add_argument('-d', '--dev', action='store_true')
args = parser.parse_args()

PATH_CONFIG = os.path.join(Path.home(), "DayBook")

if args.dev:
    file_config = "settings.ini"
else:
    file_config = os.path.join(PATH_CONFIG, "settings.ini")

if sys.platform == "win32":
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(f'home.DayBook.{info["version"]}')


class AppStart(QMainWindow):
    def __init__(self) -> None:
        """"""
        super().__init__()

        self.setWindowTitle(f"DayBook {info['version']}")
        self.setWindowIcon(QIcon(":/day_book.png"))

        self.config = Config()

        self.size_window = QDesktopWidget().screenGeometry()  # Получение разрешение экрана
        self.indent_width = int((self.size_window.width() / 2) - 400)  # Отступ по ширине

        self.setGeometry(self.indent_width, 50, 800, 800)

        self.gui_settings = SettingsWidget(parent=self, file_config=file_config)  # Окно настроек
        self.gui_about = modules.AboutWidget(parent=self)  # Окно о программе

        # Виджеты ТабВиджетов
        self.day_book = modules.DayBook.UI.DayBookStartWidget(app=self)
        self.current_task = modules.CurrentTask.UI.CurrentTaskBar(app=self)
        self.task = modules.ListTask.UI.TaskBar(parent=self)

        # ТабВиджет
        self.t_bar = QTabWidget()
        self.t_bar.setTabPosition(QTabWidget.TabPosition.West)
        self.t_bar.addTab(self.day_book, "Дневник")
        self.t_bar.addTab(self.current_task, "Текущая задача")
        self.t_bar.addTab(self.task, "Список задачи")

        # Layout
        self.layer = QHBoxLayout()
        self.layer.addWidget(self.t_bar)

        # Widget
        self.widget = QWidget()
        self.widget.setLayout(self.layer)
        self.setCentralWidget(self.widget)

        # Menu
        self.menu_bar = AppMenuBar(parent=self)

        self.setMenuBar(self.menu_bar)
        self.showMaximized()

        # ГОРЯЧИЕ КЛАВИШИ
        self.key_ctrl_s = QShortcut(QKeySequence('Ctrl+S'), self)
        self.key_ctrl_s.activated.connect(self.day_book.save_day_book)

        # Подстановка времени в запись дневника
        time_insert_key = QKeySequence(self.config.get("HotKey", "time_insert"))
        short_cut_time_insert = QShortcut(time_insert_key, self)
        short_cut_time_insert.activated.connect(self.day_book.insert_current_time)

    def update_completed_task(self):
        """
        version 2.3.7

        Обновление списка выполненных задач.
        """
        # Обновляем список выполненных задач. На странице дневника
        self.day_book.update_completed_task()
         # Обновление списка невыполненных задач в представлении "Список задач"
        self.task.task.draw_list_task()


if __name__ == "__main__":

    config = Config()
    config.check_config()
    config.check_parameters()
    del config

    app = QApplication([])
    window = AppStart()
    app.exec_()
