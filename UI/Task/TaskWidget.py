#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""

Виджет вывода списка всех задач

"""

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import modules
import UI


class TaskWidget(QWidget, modules.ORM):
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

        task = UI.Task(name_task=name_task)
        self.layout.addWidget(task)

        self.layout.addItem(self.space)

        self.databases.add(modules.Task(
            task_name=name_task,
        ))
        self.databases.commit()
