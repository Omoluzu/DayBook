#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Кнопка на запрос добавления новой текущей задачи
"""

from PyQt5.QtWidgets import QPushButton

from modules.CurrentTask import CurrentTask
from modules.ListTask import Tasks


class AdditionNewCurrentTaskButton(QPushButton):
    """
    Кнопка добавления новой задачи на выполнение.
    """
    current_task_bar: 'CurrentTaskBar'

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
