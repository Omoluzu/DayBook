#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import configparser

from PyQt5.QtWidgets import QFileDialog, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel

VERSION = "2.0.9"


class OpenFile(QFileDialog):
    def __init__(self):
        super().__init__()

        self.path_directory = self.getExistingDirectory()
        self.setDirectory("C:")

        self.path_directory = os.path.normpath(self.path_directory)


class AppGuiAbout(QWidget):

    def __init__(self, parent):
        super().__init__()

        self.parent = parent

        self.setWindowTitle("О программе")
        self.setGeometry(600, 200, 350, 100)

        # self.config = configparser.ConfigParser()
        # self.config.read('project.ini')

        self.layout = QVBoxLayout()

        self.label_name_project = QLabel("ДНЕВНИК")
        self.layout.addWidget(self.label_name_project)

        self.label_version = QLabel(f'Версия программы: {VERSION}')
        # self.label_version = QLabel(f'Версия программы: {self.config.get("GENERAL", "version")}')
        self.layout.addWidget(self.label_version)

        self.label_copyright = QLabel("Copyright: \xa9 2020 Волков Алексей")
        self.layout.addWidget(self.label_copyright)

        self.setLayout(self.layout)


        # print(self.config.get("GENERAL", "version"))


class AppGuiSettings(QWidget):

    def __init__(self, file_config):
        super().__init__()
        self.file_config = file_config
        self.setWindowTitle('Настройки программы')
        self.setGeometry(600, 300, 800, 50)

        self.config = configparser.ConfigParser()
        self.config.read(self.file_config)

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

        self.button_save_settings = QPushButton("Сохранить", self)
        self.button_save_settings.clicked.connect(self.save_settings)
        self.layout.addWidget(self.button_save_settings)

        self.setLayout(self.layout)

    def selected_path_save_directory(self):
        directory = OpenFile()
        self.text_path_save.setText(directory.path_directory)

        print(directory.path_directory)

    def save_settings(self):
        path_save = (self.text_path_save.text())

        self.config.set("OTHER", "path_save_daybook", path_save)

        with open(self.file_config, "w") as config_file:
            self.config.write(config_file)
