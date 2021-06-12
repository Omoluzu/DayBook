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

    def __init__(self):

        if not ORM.databases:
            ORM.config = Config()

            _engine = create_engine(f'sqlite:///{ORM.config.get("Databases", "path")}')

            DeclarativeBase.metadata.create_all(_engine)
            _Session = sessionmaker(bind=_engine)
            ORM.databases = _Session()
