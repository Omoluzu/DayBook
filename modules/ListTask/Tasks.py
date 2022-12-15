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

        update version 2.4.7
            - Обновление возвращаемого списка, Так же возвращаються все задачи помеченные как current_task в БД
        """

        for task in cls.databases.query(ORM.Task).all():
            if not task.completed and task.current_task:
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

    @classmethod
    def update_completed_task(cls, data):
        """
        new version 2.3.9

        Обновление строки при выполнении задачи.

        data = {
            "id": 1,
            "date_completed": 2021-09-18  # type datetime.now()
        }
        """
        task = cls.databases.query(ORM.Task).filter_by(id=data['id']).one()

        task.completed = True
        task.date_completed = data['date_completed']
        cls.databases.commit()

    @classmethod
    def update_info_task(cls, data):
        """
        Обновление информации о задачи.

        data = {
            "id": <int>,  # Ид редактируемой задачи,
            "name": <str>,  # Новое наименование задачи,
            "notes": <str>,  # Новое описание к задачи,
        }

        new version 2.4.3
        update version 2.4.6:
            Добавленно сохранение описания в указанной задаче
        """
        task = cls.databases.query(ORM.Task).filter_by(id=data['id']).one()

        task.task_name = data['name']
        task.description = data['notes']
        cls.databases.commit()

    @classmethod
    def create_task(cls, data):
        """
        Создание задач

        data = {
            "name": str(),
            "description": str(),  # Опционально
            "current_task" False,  # Опционально
        }

        new version 2.4.7
        """
        assert data.get('name'), "ORM.TASKS.create_task - Необходим обязательный параметр name"

        new_task = ORM.Task(
            task_name=data['name'],
            date_created=datetime.datetime.now().date()
        )

        if current_task := data.get('current_task'):
            new_task.current_task = current_task

        if description := data.get('description'):
            new_task.description = description

        cls.databases.add(new_task)
        cls.databases.commit()
        return new_task
