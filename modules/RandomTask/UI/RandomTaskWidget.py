#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Виджет вывода рандомных задач
"""

from PyQt5.QtWidgets import *


class RandomTaskWidget(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)
