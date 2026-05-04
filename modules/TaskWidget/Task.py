#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Виджет непосредственно самой задачи
"""
from typing import Optional, TYPE_CHECKING

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QMouseEvent, QFont
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel

from modules.CurrentTask import CurrentTask
from modules.HandBook import ChangeTaskInfoDialog, MenuCurrentTask
from modules.ListTask import Tasks

from .ButtonComplete import ButtonComplete
from .QuestionCompletedTaskDialog import QuestionCompletedTaskDialog


if TYPE_CHECKING:
    from DayBook import AppStart


class UI(QWidget):
    def __init__(self):
        super().__init__()

        p = self.palette()
        p.setColor(self.backgroundRole(), QColor(200, 200, 200, 125))
        self.setPalette(p)

        self.setAutoFillBackground(True)
        self.setFixedHeight(50)  # Фиксированный размер виджета

        self.layer = QHBoxLayout()
        self.layer.setContentsMargins(10, 0, 0, 0)

        self.label_name_task = NameTask(self.name_task)
        self.layer.addWidget(self.label_name_task)

        self.setLayout(self.layer)


class Task(UI):
    """
    Виджет задачи
    """
    notes: str
    id_task: int  # ID задачи
    name_task: str  # Название задачи
    parent_type: str

    def __init__(self, app: "AppStart", id_task: int, name_task: str, notes: str, parent_type: str):
        self.app: "AppStart" = app
        """Головное приложение"""
        self.notes = notes
        self.id_task = id_task
        self.name_task = name_task
        self.parent_type = parent_type

        super().__init__()

        btn_close_task = ButtonComplete()
        self.layer.addWidget(btn_close_task)
        btn_close_task.clicked.connect(self.action_close_task)

    def __repr__(self):
        return f"{self.__class__.__name__} - {self.id_task}: {self.name_task}"

    def mouseDoubleClickEvent(self, event):
        ChangeTaskInfoDialog(self)

    def mousePressEvent(self, a0: Optional[QMouseEvent]) -> None:
        """
        Вызов меню бара при нажатии правой кнопки мыши по задаче
        """
        if (
                a0.button() == Qt.MouseButton.RightButton
                and self.parent_type == "current"
        ):
            menu = MenuCurrentTask(task=self)
            menu.exec_(self.mapToGlobal(a0.pos()))

        super().mousePressEvent(a0)

    def action_close_task(self):
        """
        Завершение/выполнение задачи
        """
        quest = QuestionCompletedTaskDialog(id_task=self.id_task)
        quest.exec_()

        if quest.yesno:
            # Обновляем список выполненных задач. На странице дневника
            self.app.update_completed_task()
            self.close()  # Закрываем виджет с задачей

    def returned_current_task(self) -> None:
        """Возвращение задачи в бэклог задач"""
        for task in CurrentTask.get_current_task_all():
            if task.task_id == self.id_task:
                CurrentTask.deleted_current_task_by_id(id_current_task=task.id)
                self.close()
                break

    def delete_current_task(self) -> None:
        """Удаление задачи"""
        # Возвращает задачу в бэклог.
        self.returned_current_task()
        # Удаляем задачу из базы данных
        Tasks.delete_task(task_id=self.id_task)
        # Обновляем список задач
        self.app.update_completed_task()


class NameTask(QLabel):

    def __init__(self, text: str) -> None:
        super().__init__(text)

        font = QFont()
        font.setPointSize(24)
        font.setFamily("Gabriola")
        self.setFont(font)
