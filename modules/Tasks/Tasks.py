#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль для работы с Задачами.
Все запросы в БД должны выполнятся только в этом модуле
"""

import datetime


from modules import *


class Tasks(ORM.ORM):

    def get_day_complete_task(self, day: datetime = datetime.datetime.today()) -> list:
        """
        Получение выполненых задач в указаный день

        Используется в DayBookWidget для создания выполненых задач за сегодня
        """
        return self.databases.query(ORM.Task).filter_by(date_completed=day.date()).all()
