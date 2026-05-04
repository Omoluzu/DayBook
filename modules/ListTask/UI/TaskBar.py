#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Головной виджет задач
"""
from typing import TYPE_CHECKING

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea

import modules


if TYPE_CHECKING:
    from DayBook import AppStart


class TaskBar(QWidget):
    """Список задач"""

    def __init__(self, parent: "AppStart") -> None:
        super().__init__()

        layout = QVBoxLayout()

        menu = modules.ListTask.UI.TaskMenuWidget()  # Меню виджетов
        menu.createTaskSignal.connect(self.action_create_task)

        self.task = modules.ListTask.UI.TaskWidget(parent=parent)  # Виджет вывода задач

        scroll = QScrollArea()
        scroll.setWidget(self.task)
        scroll.setWidgetResizable(True)

        layout.addWidget(menu)
        layout.addWidget(scroll)

        self.setLayout(layout)

    def action_create_task(self):
        """
        Создание новой задачи

        update version 2.4.7
            - В текущий метод вынесено создание задачи
            - Удалено передача в класс CreateTaskDialog параметра self.task_bar
        """

        create_task = modules.ListTask.UI.CreateTaskDialog()
        create_task.exec_()
        if create_task:
            self.task.create_task(
                name_task=create_task.name_task.text(),
                description=create_task.description.toPlainText()
            )
