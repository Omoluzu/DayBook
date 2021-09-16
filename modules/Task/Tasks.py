#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль для работы с Задачами.
Все запросы в БД должны выполнятся только в этом модуле
"""

import random
import datetime
import sqlalchemy.exc

from modules import *


class Tasks(ORM.ORM):

    @classmethod
    def get_day_complete_task(cls, day: datetime = datetime.datetime.today()) -> list:
        """
        Получение выполненых задач в указаный день
        """
        try:
            return cls.databases.query(ORM.Task).filter_by(date_completed=day.date()).all()
        except sqlalchemy.exc.OperationalError:
            return []

    @classmethod
    def get_task_by_id(cls, id_task: int):
        """
        Возврат задачи по ИД задачи в базе данных
        """
        try:
            return cls.databases.query(ORM.Task).filter_by(id=id_task).one()
        except sqlalchemy.exc.NoResultFound:
            return " "

    @classmethod
    def get_action_task(cls) -> list:
        """
        Возврат списка активных задач
        """

        for task in cls.databases.query(ORM.Task).all():
            if not task.completed:
                yield task

    @classmethod
    def get_random_task(cls):
        """
        Возврат рандомной задачи из списка невыполненых задач
        """
        from modules.CurrentTask import CurrentTask

        task_all = set(task.id for task in cls.get_action_task())
        current_task = set(task.task_id for task in list(CurrentTask.get_current_task_all()))
        sequence = list(task_all ^ current_task)

        return random.choice(list(task_all ^ current_task)) if sequence else None
