#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль для работы с текущими задачами.
Все запросы в БД должны выполнятся только в этом модуле
"""


from modules import *
from modules.ListTask import Tasks


class CurrentTask(ORM.ORM):

    @classmethod
    def get_current_task_all(cls):
        """
        Получения всего списка задач из БД Текущей задачи
        """
        return cls.databases.query(ORM.RandomTask).all()

    @classmethod
    def get_list_current_task(cls):
        """
        Вывести список текущих задач
        """

        for current_task in CurrentTask.get_current_task_all():
            if current_task.task_id:  # Проверка указан ли ИД задачи
                task = Tasks.get_task_by_id(id_task=current_task.task_id)  # Нахождение задачи по её айди в общем списке
                if task.completed:  # Проверка на выполнение задачи
                    CurrentTask.deleted_current_task_by_id(id_current_task=current_task.id)  # Удаление связи с текущей задачеи
                else:
                    yield task  # Возвращаем задачу

    @classmethod
    def deleted_current_task_by_id(cls, id_current_task):
        """
        Удаление связи из БД
        """
        cls.databases.query(ORM.RandomTask).filter_by(id=id_current_task).delete()
        cls.databases.commit()

    @classmethod
    def add_current_task(cls, id_task):
        """
        Добавление новой задачи в БД текущих задач
        """
        if id_task:
            cls.databases.add(ORM.RandomTask(
                task_id=id_task
            ))
            cls.databases.commit()
