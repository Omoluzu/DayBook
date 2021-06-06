# -*- coding: utf-8 -*-

import os

from sqlalchemy import *
from pathlib import Path
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker
import sqlalchemy.sql.default_comparator
from sqlalchemy.ext.declarative import declarative_base

# import settings

DeclarativeBase = declarative_base()


class Task(DeclarativeBase):

    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    task_name = Column(String(120))  # Название задачи
    date_created = Column(DateTime)  # Дата создания задачи
    completed = Column(Boolean)  # Пометка об выполнении задачи
    date_completed = Column(DateTime)  # Дата завершения задачи


class ORM:
    """ Класс для работы с ORM """
    databases = None

    def __init__(self):

        if not ORM.databases:
            path = os.path.join(Path.home(), r"DayBook\sqlalchemy.db")

            _engine = create_engine(f'sqlite:///{path}')

            DeclarativeBase.metadata.create_all(_engine)
            _Session = sessionmaker(bind=_engine)
            ORM.databases = _Session()
