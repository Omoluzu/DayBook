#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Головной виджет задач
"""

from PyQt5.QtWidgets import *

import UI


class TaskBar(QWidget):

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()

        self.task = UI.TaskWidget()

        self.create_task = QPushButton("Создать задачу")
        self.create_task.clicked.connect(self.action_create_task)

        random_task = QPushButton("Рандомная задача")
        random_task.clicked.connect(self.action_select_random_task)

        self.layout.addWidget(self.task)
        self.layout.addWidget(self.create_task)
        self.layout.addWidget(random_task)

        self.setLayout(self.layout)

    def action_create_task(self):
        """ Создание новой задачи """

        create_task = UI.CreateTaskDialog(parent=self)
        create_task.exec_()

    def action_select_random_task(self):
        """ Выбор рандомной задачи """

        # list_task = list(self.task.get_action_task())
        #
        # random_task = random.choice(list_task)

        # random_task_widget = UI.RandomTaskDialog(name_task=random_task)
        random_task_widget = UI.RandomTaskDialog()
        random_task_widget.exec_()
