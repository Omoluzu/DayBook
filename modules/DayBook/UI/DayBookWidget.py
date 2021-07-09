#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont

import modules


class DayBookWidget(QWidget):
    parent: 'AppStart'
    completed_task_widget: QListWidget  # Виджет вывода списока выполненых задач

    def __init__(self, parent):
        super().__init__()

        self.parent = parent

        self.font = QFont()
        self.font.setPointSize(self.parent.config.getint("TEXT", "size"))

        layout = QVBoxLayout()

        self.text = QTextEdit()
        self.text.setText(self.parent.start_day.start())
        self.text.setReadOnly(True) if self.parent.start_day.check_read else self.text.setReadOnly(False)
        self.text.setFont(self.font)

        self.completed_task_widget = QListWidget()
        self.completed_task_widget.setFixedHeight(100)
        self.update_completed_task()

        layout.addWidget(self.text)
        layout.addWidget(QLabel("Список выполненых задач:"))
        layout.addWidget(self.completed_task_widget)

        self.setLayout(layout)

    def update_completed_task(self):
        """
        Обновление и получение списка выполненых задач
        """
        self.completed_task_widget.clear()
        for i, task in enumerate(modules.Tasks.get_day_complete_task()):
            self.completed_task_widget.addItem(f"{i + 1}. {task.task_name}")
