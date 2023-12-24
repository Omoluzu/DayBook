"""
Пункт меню для задач расположенных в файле текущая задача.
"""

from PyQt5.QtWidgets import QMenu, QAction


class MenuCurrentTask(QMenu):
    def __init__(self, task: 'Task'):
        super().__init__()

        return_action = QAction("Вернуть в Бэклог", self)
        return_action.triggered.connect(task.returned_current_task)
        self.addAction(return_action)
