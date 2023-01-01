#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Виджет непосредственно самой задачи
"""

from datetime import datetime

from PyQt5.QtWidgets import *

from modules.ListTask.Tasks import Tasks
from wrapperQWidget5.WrapperWidget import wrapper_widget

__all__ = ['QuestionCompletedTaskDialog']


class QuestionCompletedTaskDialog(QDialog):
    id_task: int  # ID выполняемой задачи
    yesno: bool  # Подтверждение выполнения задачи
    select_date: datetime.now  # Строка с датой
    calendar: 'OpenCalendar'  # Виджет календаря
    data_completed_task: QLabel  # UI поле с датой
    layouts: dict  # Инструкция создания UI для декоратора @wrapper_widget

    @wrapper_widget
    def __init__(self, id_task):
        super().__init__()

        self.id_task = id_task
        self.yesno = False
        self.select_date = datetime.now().date()
        self.calendar = OpenCalendar(self)

        no = QPushButton("НЕТ")
        no.clicked.connect(self.close)

        yes = QPushButton("ДА")
        yes.clicked.connect(self.action_yes)

        self.data_completed_task = QLabel(str(self.select_date))

        button_calendar = QPushButton("Изменить")
        button_calendar.clicked.connect(self.action_open_calendar)

        self.layouts = {
            "vbox": [
                QLabel("Подтвердите выполнение задачи"),
                {"hbox": [
                    QLabel("Дата выполнения задачи:"),
                    self.data_completed_task,
                    button_calendar
                ]},
                {"hbox": [
                    no,
                    yes
                ]},
            ]
        }

    def action_yes(self):
        """
        update version 2.3.9

        Подтвердение выполнения текущей задачи
        """
        self.yesno = True

        data = {
            "id": self.id_task,
            "date_completed": self.select_date
        }

        Tasks.update_completed_task(data)
        self.close()

    def action_open_calendar(self):
        """
        new version 2.3.9  

        Открытие календаря для изменения даты выполнения текущей задачи
        """
        self.calendar.exec_()
        self.select_date = self.calendar.select_date
        self.data_completed_task.setText(str(self.select_date))


class OpenCalendar(QDialog):

    @wrapper_widget
    def __init__(self, parent):
        super().__init__()

        self.parent = parent
        self.select_date = None

        self.calendar = QCalendarWidget()

        self.btn_cancel = QPushButton("Отмена")
        self.btn_cancel.clicked.connect(self.action_cancel)

        self.btn_save = QPushButton("Сохранить")
        self.btn_save.clicked.connect(self.action_save)

        self.layouts = {
            "vbox": [
                self.calendar,
                {"hbox": [
                    self.btn_cancel,
                    self.btn_save
                ]}
            ]
        }

    def action_cancel(self):
        self.close()

    def action_save(self):
        """ Получение выбранной даты """
        select_date = self.calendar.selectedDate()
        select_date = f"{select_date.year()}-{str(select_date.month()).zfill(2)}-{str(select_date.day()).zfill(2)}"
        self.select_date = datetime.strptime(select_date, "%Y-%m-%d").date()
        self.close()
