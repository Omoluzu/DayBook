#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""

Виджет вывода списка всех задач

"""

import datetime

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import modules
import UI


class TaskWidget(QWidget, modules.ORM):
    """
    Виджет вывода списка всех задач
    """
    space: QSpacerItem  # Выравниватель задач сверху
    layout: QVBoxLayout  # Основно лайоут для задач

    def __init__(self):
        super().__init__()

        self.setAutoFillBackground(True)

        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.white)
        self.setPalette(p)

        self.space = QSpacerItem(150, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        for task in self.databases.query(modules.Task).all():
            if not task.completed:
                self.layout.addWidget(UI.Task(id_task=task.id, name_task=task.task_name))

        self.layout.addItem(self.space)

    def create_task(self, name_task):
        """
        Создание новой задачи.

        создание и удаление space происходит ради того что когда добавлюятся новые задачи,
        они добавляются ниже space и их отображение становится не корректным

        При создании задачи происходит добавление нового виджета задачи и
        запись задачи в базу данных
        """

        # Добавление задачи в БД
        self.databases.add(modules.Task(
            task_name=name_task,
            date_created=datetime.datetime.now()
        ))
        self.databases.commit()

        # Получение последнего ИД (решения вопроса с получение ИД задачи)
        last_id_task = self.databases.query(modules.Task).order_by(modules.Task.id.desc()).first()

        # Удаляем space
        self.layout.removeItem(self.space)

        # Создаем виджет задачи и добавлего для отображения
        task = UI.Task(id_task=last_id_task.id, name_task=name_task)
        self.layout.addWidget(task)

        # Добавляем space
        self.layout.addItem(self.space)

    @classmethod
    def get_action_task(cls) -> list:
        """
        Возврат списка активных задач
        """

        for task in cls.databases.query(modules.Task).all():
            if not task.completed:
                yield task.id
