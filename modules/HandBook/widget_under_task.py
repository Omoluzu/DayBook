#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QPushButton, QLabel 
from PyQt5.QtGui import QColor
from PyQt5.QtCore import QSize

from wrapperQWidget5.WrapperWidget import wrapper_widget

from modules.ListTask.Tasks import Tasks


class UI(QWidget):
    """
    Виджет отрисовки подзадач

    new version 2.4.7
    """
    @wrapper_widget
    def __init__(self):
        super().__init__()

        p = self.palette()
        p.setColor(self.backgroundRole(), QColor(255, 200, 0, 127))
        self.setPalette(p)
        self.setAutoFillBackground(True)
        
        self.btn = QPushButton('-')
        self.btn.setFixedSize(QSize(30, 30))

        self.label_task_name = QLabel()

        self.layouts = {
            "hbox": [
                self.label_task_name,
                self.btn
            ]
        }


class UnderTaskWidget(UI):
    """
    Виджет отрисовки подзадач

    new version 2.4.7
    """
    def __init__(self, under_task):
        super().__init__()
        self.under_task = under_task
        self.btn.clicked.connect(self.action_completion_task)
        self.label_task_name.setText(self.under_task.task_name)

    def action_completion_task(self):
        """
        Активация завершения задачи

        new version 2.4.7
        """
        
        Tasks.set_finished_task(self.under_task.id)
        # print(self.under_task.id)
        self.close()



