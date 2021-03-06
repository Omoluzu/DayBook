#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Виджет непосредственно самой задачи
"""

import datetime

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from modules import *


class Task(QWidget, ORM.ORM):
    """
    Виджет задачи
    """
    parent: 'AppStart'
    id_task: int  # ID задачи
    name_task: str  # Название задачи
    db: 'ORM.Task'  # Информация о задачи в БД

    def __init__(self, parent, id_task, name_task):
        super().__init__()

        self.parent = parent
        self.id_task = id_task
        self.name_task = name_task
        self.db = self.databases.query(ORM.Task).filter_by(id=self.id_task).one()

        p = self.palette()
        p.setColor(self.backgroundRole(), QColor(200, 200, 200, 125))
        self.setPalette(p)

        self.setAutoFillBackground(True)
        self.setFixedHeight(50)  # Фиксированный размер виджета

        layout = QHBoxLayout()
        layout.setContentsMargins(10, 0, 0, 0)

        self.label_name_task = NameTask(self.name_task)
        layout.addWidget(self.label_name_task)

        btn_close_task = ButtonComplete()
        layout.addWidget(btn_close_task)
        btn_close_task.clicked.connect(self.action_close_task)

        self.setLayout(layout)

    def __repr__(self):
        return f"{self.__class__.__name__} - {self.id_task}: {self.name_task}"

    def action_close_task(self):
        """
        Завершение/выполнение задачи
        """
        quest = QuestionCompletedTaskDialog()
        quest.exec_()

        if quest.yesno:

            self.db.completed = True  # Помечаем в БД что задача выполнена
            self.db.date_completed = datetime.datetime.now().date()  # Сохраняем время выполнения задачи
            self.databases.commit()  # Сохраняем информацию в БД

            self.parent.day_book.update_completed_task()  # Обновляем список выполненых задач. На странице дневника
            self.close()  # Закрываем виджет с задачей



class QuestionCompletedTaskDialog(QDialog):
    yesno: bool  # Подтверждение выполнения задачи

    def __init__(self):
        super().__init__()
        self.yesno = False

        layout = QVBoxLayout()
        self.setLayout(layout)

        layout.addWidget(QLabel("Подтвердите выполнение задачи"))

        quest_layout = QHBoxLayout()
        layout.addLayout(quest_layout)

        no = QPushButton("НЕТ")
        quest_layout.addWidget(no)
        no.clicked.connect(self.close)

        yes = QPushButton("ДА")
        quest_layout.addWidget(yes)
        yes.clicked.connect(self.action_yes)

    def action_yes(self):
        self.yesno = True
        self.close()


class NameTask(QLabel):

    def __init__(self, text):
        super().__init__(text)

        font = QFont()
        font.setPointSize(24)
        font.setFamily("Gabriola")
        self.setFont(font)


class ButtonComplete(QPushButton):

    def __init__(self):
        super().__init__()

        self.setIcon(QIcon(":/check.png"))
        self.setIconSize(QSize(50, 50))
        self.setFixedSize(QSize(50, 50))
        self.setFlat(True)
