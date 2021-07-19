#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Виджет вывода рандомных задач
"""

from PyQt5.QtWidgets import *

from modules.CurrentTask import CurrentTask
from modules.Task import Tasks
from modules import Task


class CurrentTaskBar(QWidget):
    app: 'AppStart'

    def __init__(self, app):
        super().__init__()

        self.app = app

        layout = QVBoxLayout()
        self.setLayout(layout)

        for current_task in CurrentTask.get_list_current_task():

            if current_task.task_id:  # Проверка указан ли ИД задачи
                task = Tasks.get_task_by_id(id_task=current_task.task_id)  # Нахождение задачи по её одни в общем списке

                if task.completed:  # Проверка на выполнение задачи
                    CurrentTask.clear_current_task_by_id(id_current_task=current_task.id)  # Очищаем из текущей задачи
                else:

                    layout.addWidget(
                        Task.UI.Task(parent=self.app, id_task=task.id, name_task=task.task_name)
                    )
