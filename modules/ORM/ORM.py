# -*- coding: utf-8 -*-

from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from modules.Configuration import Config

DeclarativeBase = declarative_base()


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

