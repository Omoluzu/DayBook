#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Диалог добавления новой задачи.
"""

from PyQt5.QtWidgets import *


class CreateTaskDialog(QDialog):
    """
    Виджет добавление новой задачи
    """

    def __init__(self, parent):
        super().__init__()

        self.parent = parent

        label = QLabel("Введите название задачи")
        self.name_task = QLineEdit()

        btn = QPushButton("Создать задачу")
        btn.clicked.connect(self.action_create_task)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.layout.addWidget(label)
        self.layout.addWidget(self.name_task)
        self.layout.addWidget(btn)

    def action_create_task(self):
        """
        Добавление новой задачи
        """

        self.parent.task.create_task(name_task=self.name_task.text())
        self.close()
