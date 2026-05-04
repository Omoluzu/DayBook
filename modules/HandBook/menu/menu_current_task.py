"""
Пункт меню для задач расположенных в файле текущая задача.
"""
from typing import Any, TYPE_CHECKING

from PyQt5.QtWidgets import QMenu, QAction


if TYPE_CHECKING:
    from modules.TaskWidget import Task


class MenuCurrentTask(QMenu):
    def __init__(self, task: "Task", *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        return_action = QAction("Вернуть в Бэклог", self)
        return_action.triggered.connect(task.returned_current_task)
        self.addAction(return_action)

        delete_action = QAction("Удалить", self)
        delete_action.triggered.connect(task.delete_current_task)
        self.addAction(delete_action)
