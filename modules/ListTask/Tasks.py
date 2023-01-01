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
    def get_under_task(cls, task_id: int):
        """
        Получение списка связанных подзадач

        task_id: int() - ID  искомой задачи

        new version 2.4.7
        """
        def get_list_under_task():
            for link in cls.databases.query(ORM.LinkTask).filter_by(task_id=task_id).all():
                under_task = cls.get_task_by_id(link.under_task_id)
                if not under_task.completed:
                    yield under_task

        return list(get_list_under_task())

    @classmethod
    def set_finished_task(cls, id: int, date_complited: datetime.datetime = datetime.datetime.now().date()):
        """
        Завершения указанной в id задачи

        ::id: int - Номер задачи из базы данных
        ::date_complited: datetime.datetime - дата завершения задачи

        new version 2.4.7
        """
        cls.update_completed_task({
            "id": id,
            "date_completed": date_complited
        })

    @classmethod
    def update_completed_task(cls, data):
        """
        new version 2.3.9

        Обновление строки при выполнении задачи.

        data = {
            "id": 1,
            "date_completed": 2021-09-18  # type datetime.now().date()
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
    def create_task(cls, name, description = None, current_task = True):
        """
        Создание задач

        data = {
            "name": str(),
            "description": str(),  # Опционально
            "current_task" bool(), default False,  # Опционально
        }

        new version 2.4.7
        """
        new_task = ORM.Task(
            task_name=name,
            description=description,
            current_task = current_task,
            date_created=datetime.datetime.now().date()
        )

        cls.databases.add(new_task)
        cls.databases.commit()
        return new_task

    @classmethod
    def create_link_task(cls, task_id, under_task_id):
        """
        Создание связей для задач

        new version 2.4.7  
        """

        cls.databases.add(ORM.LinkTask(
            task_id = task_id,
            under_task_id = under_task_id
        ))
        cls.databases.commit()
