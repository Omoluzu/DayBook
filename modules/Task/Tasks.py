#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль для работы с Задачами.
Все запросы в БД должны выполнятся только в этом модуле
"""

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
