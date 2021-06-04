#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Виджет непосредственно самой задачи
"""

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import modules


class Task(QWidget, modules.ORM):
    """
    Виджет задачи
    """
    id_task: int  # ID задачи
    name_task: str  # Название задачи
    db: 'modules.ORM.Task'  # Информация о задачи в БД

    def __init__(self, id_task, name_task):
        super().__init__()

        self.id_task = id_task
        self.name_task = name_task
        self.db = self.databases.query(modules.Task).filter_by(id=self.id_task).one()

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
        return f"{self.__class__.__name__} - {self.id_task}: {self.name_task}"

    def action_close_task(self):
        """
        Завершение/выполнение задачи
        """

        self.db.completed = True  # Помечаем в БД что задача выполнена
        self.databases.commit()  # Сохраняем информацию в БД

        self.close()  # Закрываем виджет с задачей
