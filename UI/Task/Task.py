#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Виджет непосредственно самой задачи
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

        layout = QHBoxLayout()

        self.label_name_task = QLabel(self.name_task)
        layout.addWidget(self.label_name_task)

        btn_close_task = QPushButton("Close")
        layout.addWidget(btn_close_task)
        btn_close_task.clicked.connect(self.action_close_task)

        self.setLayout(layout)

    def __repr__(self):
        return f"{self.__class__.__name__} - {self.name_task}"

    def action_close_task(self):
        self.close()
