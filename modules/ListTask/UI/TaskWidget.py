#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""

Виджет вывода списка всех задач

"""

import datetime
import sqlalchemy.exc

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from modules import ORM
from modules.ListTask import Tasks
import modules


class TaskWidget(QWidget, ORM.ORM):
    """
    Виджет вывода списка всех задач
    """
    parent: 'AppStart'  # Основное приложение для связи
    layout: QVBoxLayout  # Основной лайоут для задач

    def __init__(self, parent):
        super().__init__()

        self.parent = parent

        self.setAutoFillBackground(True)

        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.white)
        self.setPalette(p)

        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignTop)

        self.draw_list_task()

    def create_task(self, name_task, description):
        """
        Создание новой задачи.

        При создании задачи происходит добавление нового виджета задачи и
        запись задачи в базу данных

        update version 2.4.1:
            - Добавлен параметр description
            - При сохранении задачи в БД, сохраняеться информация о Описании задачи (description)
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
            task = modules.TaskWidget.Task(parent=self.parent, id_task=last_id_task.id, name_task=name_task)
            self.layout.addWidget(task)

    @classmethod
    def get_action_task(cls) -> list:
        """
        Возврат списка активных задач
        """

        for task in cls.databases.query(ORM.Task).all():
            if not task.completed:
                yield task.id

    def draw_list_task(self):
        """
        version 2.3.7

        Отрисовка текущих невыполненых задач
        """
        for i in range(self.layout.count()):
            self.layout.itemAt(i).widget().deleteLater()

        for task in (list(Tasks.get_action_task())):
            task_widget = modules.TaskWidget.Task(parent=self.parent, id_task=task.id, name_task=task.task_name)
            self.layout.addWidget(task_widget)
