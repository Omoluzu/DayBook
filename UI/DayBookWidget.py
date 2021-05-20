#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QKeySequence, QFont


class DayBookWidget(QWidget):

    def __init__(self, parent):
        super().__init__()

        self.parent = parent

        self.font = QFont()
        self.font.setPointSize(self.parent.config.getint("TEXT", "size"))

        self.layout = QHBoxLayout()

        self.text = QTextEdit()
        self.text.setHtml(self.parent.start_day.start())
        self.text.setReadOnly(True) if self.parent.start_day.check_read else self.text.setReadOnly(False)
        self.text.setFont(self.font)

        self.layout.addWidget(self.text)

        self.setLayout(self.layout)