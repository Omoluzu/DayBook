#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Головной виджет задач
"""

from PyQt5.QtWidgets import *
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon

import modules


class TaskBar(QWidget):

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()

        menu = TaskMenuWidget(task_bar=self)
        self.task = modules.Tasks.UI.TaskWidget()

        scroll = QScrollArea()
        scroll.setWidget(self.task)
        scroll.setWidgetResizable(True)

        random_task = QPushButton("Рандомная задача")
        random_task.clicked.connect(self.action_select_random_task)

        self.layout.addWidget(menu)
        self.layout.addWidget(scroll)
        self.layout.addWidget(random_task)

        self.setLayout(self.layout)

    @staticmethod
    def action_select_random_task():
        """ Выбор рандомной задачи """

        random_task_widget = modules.Tasks.UI.RandomTaskDialog()
        random_task_widget.exec_()


class TaskMenuWidget(QWidget):

    def __init__(self, task_bar):
        super().__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(0, 0, 0, 0)

        space = QSpacerItem(0, 0, QSizePolicy.Minimum)

        create_task = ButtonCreateTask(task_bar=task_bar)
        layout.addWidget(create_task)
        layout.addItem(space)


class ButtonCreateTask(QPushButton):

    def __init__(self, task_bar):
        super().__init__()

        self.task_bar = task_bar

        self.setIcon(QIcon(":/create_task.png"))
        self.setIconSize(QSize(50, 50))
        self.setFixedSize(QSize(50, 50))
        self.setFlat(True)

        self.clicked.connect(self.action_create_task)

    def action_create_task(self):
        """ Создание новой задачи """

        create_task = modules.Tasks.UI.CreateTaskDialog(parent=self.task_bar)
        create_task.exec_()
