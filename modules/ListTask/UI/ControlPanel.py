from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSignal, QSize
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSpacerItem, QSizePolicy, QPushButton


class TaskMenuWidget(QWidget):
    """Панель меню для управления задачами"""
    createTaskSignal = pyqtSignal()
    """Сигнал нажатия на кнопку создания новой задачи"""

    def __init__(self) -> None:
        """Инициализация"""
        super().__init__()

        layer = QVBoxLayout(self)
        layer.setContentsMargins(0, 0, 0, 0)

        space = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum)

        create_task = ButtonCreateTask()
        create_task.clicked.connect(self.createTaskSignal.emit)

        layer.addWidget(create_task)
        layer.addItem(space)


class ButtonCreateTask(QPushButton):
    """Кнопка создания новой задачи"""

    def __init__(self) -> None:
        """Инициализация"""
        super().__init__()

        self.setIcon(QIcon(":/create_task.png"))
        self.setIconSize(QSize(50, 50))
        self.setFixedSize(QSize(50, 50))
        self.setFlat(True)
