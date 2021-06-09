# -*- coding: utf-8 -*-

from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from modules.Configuration import Config

DeclarativeBase = declarative_base()


class Task(DeclarativeBase):

    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    task_name = Column(String(120))  # Название задачи
    date_created = Column(DATE)  # Дата создания задачи
    completed = Column(Boolean)  # Пометка об выполнении задачи
    date_completed = Column(DATE)  # Дата завершения задачи


class RandomTask(DeclarativeBase):

    __tablename__ = "random_task"

    id = Column(Integer, primary_key=True, autoincrement=True)
    task_id = Column(Integer, ForeignKey(Task.id))


class ORM:
    """ Класс для работы с ORM """
    config = None
    databases = None

    def __init__(self):

        if not ORM.databases:
            ORM.config = Config()

            _engine = create_engine(f'sqlite:///{ORM.config.get("Databases", "path")}')

            DeclarativeBase.metadata.create_all(_engine)
            _Session = sessionmaker(bind=_engine)
            ORM.databases = _Session()
