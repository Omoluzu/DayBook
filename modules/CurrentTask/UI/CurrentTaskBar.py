#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Виджет вывода случайных задач
"""
from typing import TYPE_CHECKING

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSpacerItem, QSizePolicy

from modules import TaskWidget
from modules.CurrentTask import CurrentTask, UI
from modules.ListTask.UI import TaskMenuWidget, CreateTaskDialog
from modules.ListTask import Tasks


if TYPE_CHECKING:
    from DayBook import AppStart


class CurrentTaskBar(QWidget):
    """
    Таб Бар Текущей задачи
    """

    def __init__(self, app: "AppStart") -> None:
        super().__init__()

        self.app = app

        self.layer = QVBoxLayout()
        self.setLayout(self.layer)

        menu = TaskMenuWidget()
        menu.createTaskSignal.connect(self.action_create_task)

        self.current_task = CurrentTaskWidget(app=self)
        self.layer.addWidget(menu)
        self.layer.addWidget(self.current_task)

    def show_task(self):
        """
        Показать задачи на выполнение
        """

        self.layer.removeWidget(self.current_task)

        self.current_task = CurrentTaskWidget(app=self)
        self.layer.addWidget(self.current_task)

    def action_create_task(self):
        """
        Создание новой задачи

        update version 2.4.7
            - В текущий метод вынесено создание задачи
            - Удалено передача в класс CreateTaskDialog параметра self.task_bar
        """

        create_task = CreateTaskDialog()
        create_task.exec_()
        if create_task:
            # Создаем в базе данных и тут же отображаем. Кайф.
            id_task = self.app.task.task.create_task(
                name_task=create_task.name_task.text(),
                description=create_task.description.toPlainText())
            assert id_task
            CurrentTask.add_current_task(id_task=id_task)
            self.show_task()


class CurrentTaskWidget(QWidget):
    """
    Виджет вывода текущей задачи
    """
    task_bar: CurrentTaskBar

    def __init__(self, app):
        """
        """
        super(CurrentTaskWidget, self).__init__()

        self.task_bar = app

        layout = QVBoxLayout()
        self.setLayout(layout)

        for current_task in CurrentTask.get_list_current_task():
            layout.addWidget(TaskWidget.Task(
                app=self.task_bar.app, id_task=current_task.id,
                name_task=current_task.task_name,
                notes=current_task.description, parent_type='current'
            ))

        # Кнопка добавления новой задачи
        btn_new_current_task = UI.AdditionNewCurrentTaskButton(current_task_bar=self.task_bar)
        layout.addWidget(btn_new_current_task)

        space = QSpacerItem(150, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addItem(space)
