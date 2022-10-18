# -*- coding: utf-8 -*-

from sqlalchemy import *
# from sqlalchemy import MetaData
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
    description = Column(Text)  # Описание задачи
    current_task = Column(Boolean, default=True)  # Пометка о том что текущую задачу можно выводить в представлении "Список задач"


class RandomTask(DeclarativeBase):
    __tablename__ = "random_task"

    id = Column(Integer, primary_key=True, autoincrement=True)
    task_id = Column(Integer, ForeignKey(Task.id))


class ORM:
    """ Класс для работы с ORM """
    config = None
    databases = None

    if not databases:
        config = Config()

        _engine = create_engine(f'sqlite:///{config.get("Databases", "path")}')

        DeclarativeBase.metadata.create_all(_engine)
        _Session = sessionmaker(bind=_engine)
        databases = _Session()


if __name__ == "__main__":
    ORM()

