#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import *


class AboutWidget(QWidget):

    def __init__(self, parent):
        super().__init__()

        from DayBook import VERSION

        self.parent = parent

        self.setWindowTitle("О программе")
        self.setGeometry(600, 200, 350, 100)

        self.layout = QVBoxLayout()

        self.label_name_project = QLabel("ДНЕВНИК")
        self.layout.addWidget(self.label_name_project)

        self.label_version = QLabel(f'Версия программы: {VERSION}')
        self.layout.addWidget(self.label_version)

        self.label_copyright = QLabel("Copyright: \xa9 2020-2021 Волков Алексей")
        self.layout.addWidget(self.label_copyright)

        self.setLayout(self.layout)