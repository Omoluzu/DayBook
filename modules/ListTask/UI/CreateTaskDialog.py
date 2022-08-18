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
    def __init__(self, parent):
        """

        update version 2.4.1:
            - Использован декоратор wrapper_widget
            - добавлено поле для ввода описания задачи
        """

        super().__init__()

        self.parent = parent
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

    def action_create_task(self):
        """
        Добавление новой задачи

        update version 2.4.1
            - Передача информации об описании задачи
        """

        self.parent.task.create_task(
            name_task=self.name_task.text(),
            description=self.description.toPlainText()
        )
        self.close()
