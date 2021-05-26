#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""

Виджет вывода списка всех задач

"""

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class Task(QWidget):
    """
    Виджет задачи
    """

    def __init__(self, name_task):
        super().__init__()

        self.name_task = name_task

        self.setAutoFillBackground(True)

        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.red)
        self.setPalette(p)

        self.setFixedHeight(50)

        self.layout = QHBoxLayout()

        text = QLabel(self.name_task)
        self.layout.addWidget(text)

        self.setLayout(self.layout)


class TaskWidget(QWidget):
    """
    Виджет вывода списка всех задач
    """

    def __init__(self):
        super().__init__()

        self.setAutoFillBackground(True)

        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.green)
        self.setPalette(p)

        self.space = QSpacerItem(150, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.layout.addItem(self.space)

    def create_task(self, name_task):
        """
        Создание новой задачи.
        """

        self.layout.removeItem(self.space)

        task = Task(name_task=name_task)
        self.layout.addWidget(task)

        self.layout.addItem(self.space)
