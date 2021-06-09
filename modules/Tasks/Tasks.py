#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль для работы с Задачами.
Все запросы в БД должны выполнятся только в этом модуле
"""

import datetime

import modules
from modules import ORM


class Tasks(ORM):

    def get_day_complete_task(self, day: datetime = datetime.datetime.today()) -> list:
        """
        Получение выполненых задач в указаный день

        Используется в DayBookWidget для создания выполненых задач за сегодня
        """
        return self.databases.query(modules.Task).filter_by(date_completed=day.date()).all()
