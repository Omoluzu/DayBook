#! /usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

from ico import recource


class AboutWidget(QWidget):

    def __init__(self, parent):
        super().__init__()

        from versions import info

        self.parent = parent

        self.setWindowTitle("О программе")
        self.setGeometry(600, 200, 350, 100)
        self.setWindowIcon(QIcon(":/day_book.png"))

        self.layer = QVBoxLayout()

        self.label_name_project = QLabel("ДНЕВНИК")
        self.layer.addWidget(self.label_name_project)

        self.label_version = QLabel(f'Версия программы: {info["version"]}')
        self.layer.addWidget(self.label_version)

        self.label_copyright = QLabel(f"Copyright: \xa9 2020-{datetime.now().year} Волков Алексей")
        self.layer.addWidget(self.label_copyright)

        self.setLayout(self.layer)
