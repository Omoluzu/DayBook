#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Виджет редактирования задач
"""

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from wrapperQWidget5.WrapperWidget import wrapper_widget

from modules.ListTask.Tasks import Tasks


class UI(QDialog):


    @wrapper_widget
    def __init__(self):
        super().__init__()

        # self.setWindowTitle(str(self.task.id_task))
        self.setFixedSize(304, 415)

        self.name_task = QLineEdit()
        self.notes_task = QTextEdit()

        self.btn_save = QPushButton("Сохранить")

        self.btn_hide = QPushButton(">")
        self.btn_hide.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.btn_hide.setMaximumWidth(20)

        self.under_task_widget = QWidget()
        self.under_task_widget.setFixedSize(434, 415)
        self.under_task_widget.setVisible(False)

        self.layouts = {
            "hbox": [
                {"config": {
                    "margin": 0
                }},

                {"vbox": [
                    self.name_task,
                    self.notes_task,
                    self.btn_save
                ]},
                self.btn_hide,
                self.under_task_widget
            ]
        }


class ChangeTaskInfoDialog(UI):
    """
    Виджет редактирования информации по задаче
    """

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
            - Отрисовка графики выведен в отдельный класс
        """
        super().__init__()
        self.task = task

        self.name_task.setText(self.task.name_task)
        self.notes_task.setText(self.task.notes)

        self.btn_save.clicked.connect(self.action_save_info_task)
        self.btn_hide.clicked.connect(self.action_show_under_task)

    def action_show_under_task(self):
        """
        Активация кнопки управления видимостью под задач

        new version 2.4.7
        """
        if self.btn_hide.text() == ">":
            self.setFixedSize(744, 415)
            self.under_task_widget.setVisible(True)
            self.btn_hide.setText("<")
        else:
            self.setFixedSize(304, 415)
            self.under_task_widget.setVisible(False)
            self.btn_hide.setText(">")


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

