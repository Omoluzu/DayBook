#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import datetime
import configparser

from PyQt5.QtWidgets import (
    QFileDialog, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QLabel, QCalendarWidget
)


def create_option_config(file_config, section, option, key):
    """ Обновление """
    config = configparser.ConfigParser()
    config.read(file_config)
    config.set(section, option, key)

    with open(file_config, "w") as config_file:
        config.write(config_file)


class OpenCalendar(QWidget):
    def __init__(self, parent):
        super().__init__()

        self.parent = parent
        self.select_date = None

        self.setWindowTitle("Выбор даты начала ведения дневника")

        self.layout = QVBoxLayout()

        self.calendar = QCalendarWidget()
        self.layout.addWidget(self.calendar)

        self.btn_layout = QHBoxLayout()
        self.layout.addLayout(self.btn_layout)

        self.btn_cancel = QPushButton("Отмена")
        self.btn_cancel.clicked.connect(self.action_cancel)
        self.btn_layout.addWidget(self.btn_cancel)

        self.btn_save = QPushButton("Сохранить")
        self.btn_save.clicked.connect(self.action_save)
        self.btn_layout.addWidget(self.btn_save)

        self.setLayout(self.layout)

    def action_cancel(self):
        self.close()

    def action_save(self):
        """ Получение выбранной даты """
        select_date = self.calendar.selectedDate()
        self.select_date = f"{select_date.year()}-{select_date.month()}-{select_date.day()}"
        self.parent.text_days_of.setText(self.select_date)
        self.close()


class OpenFile(QFileDialog):
    def __init__(self, file_name=None):
        super().__init__()

        self.path_directory = self.getExistingDirectory()
        self.setDirectory("C:")

        self.path_directory = os.path.normpath(self.path_directory)
        if file_name:
            self.path_directory = os.path.join(self.path_directory, file_name)


class SettingsWidget(QWidget):

    def __init__(self, parent, file_config):
        super().__init__()

        self.parent = parent
        self.file_config = file_config
        self.setWindowTitle('Настройки программы')
        self.setGeometry(600, 300, 800, 50)

        self.config = configparser.ConfigParser()
        self.config.read(self.file_config)

        self.gui_calendar = OpenCalendar(parent=self)  # Окно о программе

        self.layout = QVBoxLayout()

        self.h1_layout = QHBoxLayout()
        self.layout.addLayout(self.h1_layout)

        self.label_path_save = QLabel("Путь хранения файлов ... ")
        self.h1_layout.addWidget(self.label_path_save)

        self.text_path_save = QLineEdit()
        self.text_path_save.setText(self.config.get("OTHER", "path_save_daybook"))
        self.text_path_save.setReadOnly(True)
        self.h1_layout.addWidget(self.text_path_save)

        self.btn_path_save = QPushButton("Выбрать", self)
        self.btn_path_save.clicked.connect(self.selected_path_save_directory)
        self.h1_layout.addWidget(self.btn_path_save)

        self.h2_layout = QHBoxLayout()
        self.layout.addLayout(self.h2_layout)

        self.label_days_of = QLabel("Старт начала ведения дневника: ")
        self.h2_layout.addWidget(self.label_days_of)

        if not self.config.has_option("OTHER", "days_of"):
            create_option_config(file_config, "OTHER", "days_of", str(datetime.datetime.now().date()))
            self.config.read(self.file_config)

        self.text_days_of = QLineEdit()
        self.text_days_of.setText(self.config.get("OTHER", "days_of"))
        self.h2_layout.addWidget(self.text_days_of)

        self.btn_days_of = QPushButton('Выбрать дату')
        self.btn_days_of.clicked.connect(self.selected_day_of)
        self.h2_layout.addWidget(self.btn_days_of)

        self.h3_layout = QHBoxLayout()
        self.layout.addLayout(self.h3_layout)

        self.label_size_text = QLabel("Размер шрифта: ")
        self.h3_layout.addWidget(self.label_size_text)

        self.text_size_text = QLineEdit()
        self.h3_layout.addWidget(self.text_size_text)
        self.text_size_text.setText(self.config.get("TEXT", "size"))

        self.h4_layout = QHBoxLayout()
        self.layout.addLayout(self.h4_layout)

        self.label_path_save_db = QLabel("путь хранения базы данных")
        self.h4_layout.addWidget(self.label_path_save_db)

        self.text_path_save_db = QLineEdit()
        self.text_path_save_db.setText(self.config.get("Databases", "path"))
        self.text_path_save_db.setReadOnly(True)
        self.h4_layout.addWidget(self.text_path_save_db)

        self.btn_path_save_db = QPushButton("Выбрать", self)
        self.btn_path_save_db.clicked.connect(self.selected_path_save_db)
        self.h4_layout.addWidget(self.btn_path_save_db)

        h5_layout = QHBoxLayout()
        self.layout.addLayout(h5_layout)

        label_hotkey_time_insert = QLabel("Горячие клавиши на подстановку времени в дневник")
        h5_layout.addWidget(label_hotkey_time_insert)

        self.text_hotkey_time_insert = QLineEdit()
        self.text_hotkey_time_insert.setText(self.config.get("HotKey", "time_insert"))
        h5_layout.addWidget(self.text_hotkey_time_insert)

        # СОХРАНИТЬ
        self.button_save_settings = QPushButton("Сохранить", self)
        self.button_save_settings.clicked.connect(self.save_settings)
        self.layout.addWidget(self.button_save_settings)

        self.setLayout(self.layout)

    def selected_path_save_directory(self):
        directory = OpenFile()
        self.text_path_save.setText(directory.path_directory)

    def selected_path_save_db(self):
        directory = OpenFile(file_name='DayBook.db')
        self.text_path_save_db.setText(directory.path_directory)

    def selected_day_of(self):
        self.gui_calendar.show()

    def save_settings(self):

        self.config.set("OTHER", "path_save_daybook", self.text_path_save.text())
        self.config.set("OTHER", "days_of", self.text_days_of.text())
        self.config.set("TEXT", "size", self.text_size_text.text())
        self.config.set("Databases", "path", self.text_path_save_db.text())
        self.config.set("HotKey", "time_insert", self.text_hotkey_time_insert.text())

        with open(self.file_config, "w") as config_file:
            self.config.write(config_file)
