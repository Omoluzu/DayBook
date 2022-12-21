#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Виджет редактирования задач
"""

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt

from wrapperQWidget5.WrapperWidget import wrapper_widget

from modules.ListTask.Tasks import Tasks
from modules.ListTask.UI.CreateTaskDialog import CreateTaskDialog


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

        self.under_layout = QVBoxLayout(self.under_task_widget)
        self.under_layout.setAlignment(Qt.AlignTop)

        self.btn_under_task_create = QPushButton("Создать")

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
    
    def draw_under_task(self):
        """
        Отрисовка виджета задач

        new version 2.4.7
        """
        #for under_task in ["1", "2", "3"]:
        #    self.under_layout.addWidget(QLabel(under_task))
        self.under_layout.addWidget(self.btn_under_task_create)


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
        self.btn_under_task_create.clicked.connect(self.action_create_under_task)

        self.draw_under_task()

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

    def action_create_under_task(self):
        """
        Активация создания новой задачи

        new version 2.4.7
        """
        new_task = CreateTaskDialog()
        new_task.exec_()

        if new_task:
            print(new_task.name_task.text())

        # ToDo: Как обычно создаем запись в БД в таблицу tasks, но выставлея флаг curent_task
            new_under_task = Tasks.create_task({
                "name": new_task.name_task.text(),
                "description": new_task.description.toPlainText()
            }) 
            print(new_under_task.id)
        # ToDo: Создаеть запись в БД в таблицу link_task
        


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

