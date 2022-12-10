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

# from .ButtonComplete import *
# from .QuestionCompletedTaskDialog import *
# from modules.ListTask.Tasks import Tasks


class ChangeTaskInfoDialog(QDialog):
    """
    Виджет редактирования информации по задаче
    """

    @wrapper_widget
    def __init__(self, task: 'Task'):
        """
        init version 2.4.0
        update version 2.4.2
            - Добавленна кнопка Сохранения информации по задачи.
        update version 2.4.3
            - Добавленна возможность изменения названия задачи.
        update version 2.4.6
            - Добавлена выджет для описания задачи
        update version 2,4,7
            - Диалог переехал в новую структуру
            - Диалог был переименован с TaskDialog в ChangeTaskInfoDialog
        """
        super().__init__()
        self.task = task

        self.setWindowTitle(str(self.task.id_task))

        self.name_task = QLineEdit(self.task.name_task)
        self.notes_task = QTextEdit(self.task.notes)

        btn_save = QPushButton("Сохранить")
        btn_save.clicked.connect(self.action_save_info_task)

        self.layouts = {
            "vbox": [
                self.name_task,
                self.notes_task,
                btn_save
            ]
        }

    def action_save_info_task(self):
        """
        Активация кнопки сохранения информации по задачи

        init version 2.4.2
        update version 2.4.3
            - Реализован запрос на изменение информации о наименовании задачи.
        update version 2.4.4
            - Реализзация автоматического обновления информации по задачи в представлении "Список задач",
                после редактирования
        update version 2.4.5
            - Реализзация автоматического обновления информации по задачи в представлении "Текущая задача",
                после редактирования
        update version 2.4.6
            - Передача информации на обновлении описания к задачи в БД.
        """
        data = {
            "id": self.task.id_task,
            "name": self.name_task.text(),
            "notes": self.notes_task.toPlainText()
        }

        Tasks.update_info_task(data)  # Обновление информации в базе данных

        self.task.parent.task.task.draw_list_task()  # Обновление списка задач в представление "Список задач"
        self.task.parent.current_task.show_task()  # Обновление списка задач в представление "Текущая задача"

        self.close()


