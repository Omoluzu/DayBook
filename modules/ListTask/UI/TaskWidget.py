#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""

Виджет вывода списка всех задач

"""

import datetime
from typing import Iterable

import sqlalchemy.exc
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout

from modules import ORM
from modules.ListTask import Tasks

import modules


class TaskWidget(QWidget, ORM.ORM):
    """
    Виджет вывода списка всех задач
    """
    def __init__(self, parent: 'AppStart') -> None:
        super().__init__()

        self.parent = parent
        """Родительский виджет"""

        self.setAutoFillBackground(True)

        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.GlobalColor.white)
        self.setPalette(p)

        self.layer = QVBoxLayout(self)
        """Основной слой для задач"""
        self.layer.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.draw_list_task()

    def create_task(self, name_task, description):
        """
        Создание новой задачи.

        При создании задачи происходит добавление нового виджета задачи и
        запись задачи в базу данных
        """

        # Добавление задачи в БД
        try:
            self.databases.add(ORM.Task(
                task_name=name_task,
                description=description,
                date_created=datetime.datetime.now().date()
            ))
            self.databases.commit()
        except sqlalchemy.exc.OperationalError:
            print("sqlalchemy.exc.OperationalError")
        except sqlalchemy.exc.PendingRollbackError:
            print("sqlalchemy.exc.PendingRollbackError")
        else:
            # Получение последнего ИД (решения вопроса с получение ИД задачи)
            last_id_task = self.databases.query(ORM.Task).order_by(ORM.Task.id.desc()).first()

            # Создаем виджет задачи и добавлего для отображения
            task = modules.TaskWidget.Task(
                app=self.parent,
                id_task=last_id_task.id,
                name_task=name_task,
                notes=description,
                parent_type=''
            )
            self.layer.addWidget(task)

    @classmethod
    def get_action_task(cls) -> Iterable[int]:
        """Возврат списка активных задач

        Returns:
            Генератор ИД не выполненных задач
        """

        for task in cls.databases.query(ORM.Task).all():
            if not task.completed:
                yield task.id

    def draw_list_task(self) -> None:
        """
        Отрисовка текущих не выполненных задач
        """
        for i in range(self.layer.count()):
            self.layer.itemAt(i).widget().deleteLater()

        for task in list(Tasks.get_action_task()):
            task_widget = modules.TaskWidget.Task(
                app=self.parent, id_task=task.id,
                name_task=task.task_name, notes=task.description,
                parent_type="backlog"
            )
            self.layer.addWidget(task_widget)
