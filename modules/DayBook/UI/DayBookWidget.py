#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import datetime

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont
from pathlib import Path


from modules.DayBook.TextDay import StartDay
import modules

PATH_CONFIG = os.path.join(Path.home(), "DayBook")
FILE_CONFIG = os.path.join(PATH_CONFIG, "settings.ini")


class DayBookStartWidget(QWidget):
    """
    Появлися в версии 2.3.4

    Стартовый виджет вывода самого дневника.
    Необходим был для создания в нем таб виджета.

    Является транзитом и передает все команды для текущей записи.

    """

    app: 'AppStart'
    current_day_book: 'DayBookWidget'

    def __init__(self, app):
        super().__init__()
        self.app = app

        # Таб Виджет
        tab = QTabWidget()
        self.current_day_book = DayBookWidget(app=self.app)
        tab.addTab(self.current_day_book, str(datetime.datetime.now().date()))

        # Добавление виджетов
        layout = QVBoxLayout()
        layout.addWidget(tab)
        self.setLayout(layout)

    def insert_current_time(self):
        """ Транзит для подставления текущего времени в дневник """
        self.current_day_book.insert_current_time()

    def update_completed_task(self):
        """ Транизит для обновления списка выполненых задач """
        self.current_day_book.update_completed_task()

    def save_day_book(self):
        """ Транизи для сохранение записей дневника """
        self.current_day_book.save_day_book()


class DayBookWidget(QWidget):
    app: 'AppStart'
    text: QTextEdit  # Виджет вывода записей дневнка
    completed_task_widget: QListWidget  # Виджет вывода списока выполненых задач
    start_day: StartDay

    def __init__(self, app):
        super().__init__()

        self.app = app

        # Настройки виджета
        self.font = QFont()
        self.font.setPointSize(self.app.config.getint("TEXT", "size"))

        self.start_day = StartDay(file_config=FILE_CONFIG, parent=self)

        # Текст
        self.text = QTextEdit()
        self.text.setText(self.start_day.start())
        self.insert_current_time()
        self.text.setReadOnly(True) if self.start_day.check_read else self.text.setReadOnly(False)
        self.text.setFont(self.font)

        # Список выполненых задач
        self.completed_task_widget = QListWidget()
        self.completed_task_widget.setFixedHeight(100)
        self.update_completed_task()

        # Добавление виджетов
        layout = QVBoxLayout()
        layout.addWidget(self.text)
        layout.addWidget(QLabel("Список выполненых задач:"))
        layout.addWidget(self.completed_task_widget)
        self.setLayout(layout)

    def update_completed_task(self):
        """
        Обновление и получение списка выполненых задач
        """
        self.completed_task_widget.clear()
        for i, task in enumerate(modules.Tasks.get_day_complete_task()):
            self.completed_task_widget.addItem(f"{i + 1}. {task.task_name}")

    def insert_current_time(self):
        """
        Подставка текущего времени в дневник
        """
        current_time = datetime.datetime.now().time().strftime("%H:%M")
        text = f"{self.text.toPlainText()}\n\n{current_time}"
        self.text.setPlainText(text)

    def save_day_book(self):
        """ Транизи для сохранение записей дневника """
        self.start_day.save()

