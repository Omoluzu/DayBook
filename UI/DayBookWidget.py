#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QKeySequence, QFont

import modules


class DayBookWidget(QWidget):

    def __init__(self, parent):
        super().__init__()

        self.parent = parent
        self.tasks = modules.Tasks.Tasks()

        self.font = QFont()
        self.font.setPointSize(self.parent.config.getint("TEXT", "size"))

        layout = QVBoxLayout()

        self.text = QTextEdit()
        self.text.setHtml(self.parent.start_day.start())
        self.text.setReadOnly(True) if self.parent.start_day.check_read else self.text.setReadOnly(False)
        self.text.setFont(self.font)

        completed_task = QListWidget()
        completed_task.setFixedHeight(100)
        for i, task in enumerate(self.tasks.get_day_complete_task()):
            completed_task.addItem(f"{i + 1}. {task.task_name}")

        # completed_task.addAction()

        layout.addWidget(self.text)
        layout.addWidget(QLabel("Список выполненых задач:"))
        layout.addWidget(completed_task)

        self.setLayout(layout)
