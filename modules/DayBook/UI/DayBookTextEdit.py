#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime

from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtGui import QFont

from modules.Configuration import Config
from modules.DayBook.TextDay import StartDay


class DayBookTextEdit(QTextEdit):
    """
    Появлися в версии 2.3.5

    Виджет вывода текстовой записи дневника.
    И работы с текстовой записью дневнка
    """
    app: 'AppStart'
    start_day: StartDay

    def __init__(self, app):
        super().__init__()

        config = Config()
        self.start_day = StartDay(parent=self)

        # Настройки виджета
        font = QFont()
        font.setPointSize(int(config.get("TEXT", "size")))

        # Текст
        self.setText(self.start_day.start())
        self.insert_current_time()
        self.setReadOnly(True) if self.start_day.check_read else self.setReadOnly(False)
        self.setFont(font)

    def insert_current_time(self):
        """
        Подставка текущего времени в дневник
        """
        current_time = datetime.datetime.now().time().strftime("%H:%M")
        text = f"{self.toPlainText()}\n\n{current_time}"
        self.setPlainText(text)

    def save_day_book(self):
        """ Транизи для сохранение записей дневника """
        self.start_day.save()
