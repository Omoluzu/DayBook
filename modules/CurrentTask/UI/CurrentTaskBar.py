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
    layout: QVBoxLayout
    app: 'AppStart'

    def __init__(self, app):
        super().__init__()

        self.app = app

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.w = CurrentTaskWidget(app=self)
        self.layout.addWidget(self.w)

    def show_task(self):
        """
        Показать задачи на выполнение
        """

        self.layout.removeWidget(self.w)

        self.w = CurrentTaskWidget(app=self)
        self.layout.addWidget(self.w)


class CurrentTaskWidget(QWidget):
    task_bar: CurrentTaskBar

    def __init__(self, app):
        super(CurrentTaskWidget, self).__init__()

        self.task_bar = app

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        for current_task in CurrentTask.get_list_current_task():
            self.layout.addWidget(Task.UI.Task(
                parent=self.task_bar.app, id_task=current_task.id, name_task=current_task.task_name)
            )

        # Кнопка добавления новой задачи
        self.btn_new_current_task = AdditionNewCurrentTaskButton(current_task_bar=self.task_bar)
        self.layout.addWidget(self.btn_new_current_task)


class AdditionNewCurrentTaskButton(QPushButton):
    """
    Кнопка добавления новой задачи на выполнение.
    """
    current_task_bar: CurrentTaskBar

    def __init__(self, current_task_bar):
        super().__init__('Добавить задачу на выполнение')

        self.current_task_bar = current_task_bar
        self.clicked.connect(self.action_clicked)

    def action_clicked(self):
        """
        Активация кнопки на добавление новой задачи на выполнение
        """
        CurrentTask.add_current_task(id_task=Tasks.get_random_task())
        self.current_task_bar.show_task()
