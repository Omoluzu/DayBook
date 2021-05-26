#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import UI


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

        self.layout = QVBoxLayout()

        self.setLayout(self.layout)

    def create_task(self, name_task):
        """
        Создание новой задачи.
        """
        task = Task(name_task=name_task)
        self.layout.addWidget(task)


class TaskBar(QWidget):

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()

        self.task = TaskWidget()

        self.create_task = QPushButton("Создать задачу")
        self.create_task.clicked.connect(self.action_create_task)

        self.layout.addWidget(self.task)
        self.layout.addWidget(self.create_task)

        self.setLayout(self.layout)

    def action_create_task(self):
        """ Создание новой задачи """

        create_task = UI.CreateTaskDialog(parent=self)
        create_task.exec_()
