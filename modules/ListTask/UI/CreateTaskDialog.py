#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Диалог добавления новой задачи.
"""

from PyQt5.QtWidgets import *
from wrapperQWidget5.WrapperWidget import wrapper_widget


class CreateTaskDialog(QDialog):
    """
    Виджет добавление новой задачи
    """

    @wrapper_widget
    def __init__(self):
        """

        update version 2.4.1:
            - Использован декоратор wrapper_widget
            - добавлено поле для ввода описания задачи
        update version 2.4.7:
            - Удалено получение параметра parent
            - Добавлен параметр для self.__create для проверки создания новой задачи
        """

        super().__init__()

        self.__create = False
        self.name_task = QLineEdit()
        self.description = QTextEdit()

        btn = QPushButton("Создать задачу")
        btn.clicked.connect(self.action_create_task)

        self.layouts = {
            "vbox": [
                QLabel("Введите название задачи"),
                self.name_task,
                self.description,
                btn
            ]
        }

    def __bool__(self):
        """
        Проверка на создание новой задачи

        new version 2.4.7
        """
        return self.__create

    def action_create_task(self):
        """
        Добавление новой задачи

        update version 2.4.1
            - Передача информации об описании задачи
        update version 2.4.7:
            - Метод теперь не создает задачу. Он лишь закрывает виджет
            - Изменение состояния флага self.create
        """
        self.__create = True
        self.close()
