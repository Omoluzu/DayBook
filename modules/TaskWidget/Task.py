#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Виджет непосредственно самой задачи
"""

import datetime
from ico import recource

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from wrapperQWidget5.WrapperWidget import wrapper_widget

from .ButtonComplete import *
from .QuestionCompletedTaskDialog import *
from modules.ListTask.Tasks import Tasks


class Task(QWidget):
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
        # self.db = self.databases.query(ORM.Task).filter_by(id=self.id_task).one()

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

    def mouseDoubleClickEvent(self, event):
        dialog = TaskDialog(self)
        dialog.exec_()

    def action_close_task(self):
        """
        Завершение/выполнение задачи
        """
        quest = QuestionCompletedTaskDialog(id_task=self.id_task)
        quest.exec_()

        if quest.yesno:
            self.parent.update_completed_task()  # Обновляем список выполненых задач. На странице дневника
            self.close()  # Закрываем виджет с задачей


class TaskDialog(QDialog):
    """
    Виджет редактирования информации по задаче

    init version 2.4.0
    update version 2.4.2
        - Добавленна кнопка Сохранения информации по задачи.
    update version 2.4.3
        - Добавленна возможность изменения названия задачи.
    """

    @wrapper_widget
    def __init__(self, task: Task):
        super(TaskDialog, self).__init__()
        self.task = task

        self.setWindowTitle(str(self.task.id_task))

        self.name_task = QLineEdit(self.task.name_task)

        btn_save = QPushButton("Сохранить")
        btn_save.clicked.connect(self.action_save_info_task)

        self.layouts = {
            "vbox": [
                self.name_task,
                btn_save
            ]
        }

    def action_save_info_task(self):
        """
        Активация кнопки сохранения информации по задачи

        init version 2.4.2
        update version 2.4.3
            - Реализован запрос на изменение информации о наименовании задачи.
        """
        data = {
            "id": self.task.id_task,
            "name": self.name_task.text()
        }

        Tasks.update_info_task(data)

        self.close()


class NameTask(QLabel):

    def __init__(self, text):
        super().__init__(text)

        font = QFont()
        font.setPointSize(24)
        font.setFamily("Gabriola")
        self.setFont(font)


