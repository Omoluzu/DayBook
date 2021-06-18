#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""

Виджет вывода списка всех задач

"""

import datetime
import sqlalchemy.exc

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from modules import *
import modules


class TaskWidget(QWidget, ORM.ORM):
    """
    Виджет вывода списка всех задач
    """
    layout: QVBoxLayout  # Основной лайоут для задач

    def __init__(self):
        super().__init__()

        self.setAutoFillBackground(True)

        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.white)
        self.setPalette(p)

        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignTop)

        try:
            for task in self.databases.query(ORM.Task).all():
                if not task.completed:
                    self.layout.addWidget(modules.Task.UI.Task(id_task=task.id, name_task=task.task_name))
        except sqlalchemy.exc.OperationalError:
            print("sqlalchemy.exc.OperationalError")

    def create_task(self, name_task):
        """
        Создание новой задачи.

        При создании задачи происходит добавление нового виджета задачи и
        запись задачи в базу данных
        """

        # Добавление задачи в БД
        try:
            self.databases.add(ORM.Task(
                task_name=name_task,
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
            task = modules.Task.UI.Task(id_task=last_id_task.id, name_task=name_task)
            self.layout.addWidget(task)

    @classmethod
    def get_action_task(cls) -> list:
        """
        Возврат списка активных задач
        """

        for task in cls.databases.query(ORM.Task).all():
            if not task.completed:
                yield task.id
