#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Диалог вывода рандомной задачи
"""

from PyQt5.QtWidgets import *


class RandomTaskDialog(QDialog):

    def __init__(self, name_task):
        super().__init__()

        layout = QHBoxLayout()
        self.setLayout(layout)

        label_task = QLabel(name_task)
        layout.addWidget(label_task)
