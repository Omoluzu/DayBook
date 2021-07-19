#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль для работы с текущими задачами.
Все запросы в БД должны выполнятся только в этом модуле
"""


from modules import *


class CurrentTask(ORM.ORM):

    @classmethod
    def get_list_current_task(cls):
        """
        Вывести список текущих задач
        """

        return cls.databases.query(ORM.RandomTask).all()

    @classmethod
    def clear_current_task_by_id(cls, id_current_task):
        """
        Очистить текущую задачу из таблицы текущих задач
        """

        current_task = cls.databases.query(ORM.RandomTask).filter_by(id=id_current_task).one()
        current_task.task_id = None
        cls.databases.commit()
