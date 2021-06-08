#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Диалог вывода рандомной задачи
"""

import random

from PyQt5.QtWidgets import *

import modules
import UI


class RandomTaskDialog(QDialog, modules.ORM):
    label_task: QLabel  # Label имени рандомной задачи

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.label_task = QLabel(" ")
        layout.addWidget(self.label_task)

        btn_post_task = QPushButton("Получить рандомнцю задачу")
        layout.addWidget(btn_post_task)
        btn_post_task.clicked.connect(self.action_random_task)

    def action_random_task(self):

        list_task = list(UI.TaskWidget.get_action_task())
        random_task = random.choice(list_task)
        self.label_task.setText(random_task)
