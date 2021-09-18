#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Виджет вывода рандомных задач
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSpacerItem, QSizePolicy

from modules.CurrentTask import CurrentTask, UI
from modules import TaskWidget


class CurrentTaskBar(QWidget):
    """
    Таб Бар Текущей задачи
    """
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
    """
    Виджет вывода текущей задачи
    """
    task_bar: CurrentTaskBar

    def __init__(self, app):
        super(CurrentTaskWidget, self).__init__()

        self.task_bar = app

        layout = QVBoxLayout()
        self.setLayout(layout)

        for current_task in CurrentTask.get_list_current_task():
            layout.addWidget(TaskWidget.Task(
                parent=self.task_bar.app, id_task=current_task.id, name_task=current_task.task_name)
            )

        # Кнопка добавления новой задачи
        btn_new_current_task = UI.AdditionNewCurrentTaskButton(current_task_bar=self.task_bar)
        layout.addWidget(btn_new_current_task)

        space = QSpacerItem(150, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addItem(space)
