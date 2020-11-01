#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import configparser

from PyQt5.QtWidgets import QMenuBar, QMenu, QAction


class AppMenuBar(QMenuBar):

    def __init__(self, parent):
        super().__init__()

        self.parent = parent

        # Menu - Файл
        self.menu_bar_file = QMenu("Файл")
        self.addMenu(self.menu_bar_file)

        self.menu_bar_file_save = QAction("Сохранить (Ctrl+S)", self.menu_bar_file)
        self.menu_bar_file_save.triggered.connect(self.parent.start_day.save)
        self.menu_bar_file.addAction(self.menu_bar_file_save)

        self.menu_bar_file.addSeparator()

        self.menu_bar_file_settings = QAction("Настройки", self.menu_bar_file)
        self.menu_bar_file_settings.triggered.connect(self.action_setting_show)
        self.menu_bar_file.addAction(self.menu_bar_file_settings)

        # Menu - Помощь
        self.menu_bar_help = QMenu("Помощь")
        self.addMenu(self.menu_bar_help)

        self.menu_bar_help_about = QAction("О программе", self.menu_bar_help)
        self.menu_bar_help_about.triggered.connect(self.action_about_show)
        self.menu_bar_help.addAction(self.menu_bar_help_about)

    def action_setting_show(self):
        """
        Открываем новое окно с настройками приложений
        """
        self.parent.gui_settings.show()

    def action_about_show(self):
        """
        Открываем новое окно с информацией о проекте
        """
        self.parent.gui_about.show()
