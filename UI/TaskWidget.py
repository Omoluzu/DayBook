#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

# class GroupWidget(QWidget):
#
#     def __init__(self):
#         super().__init__()
#
#         self.layout = QVBoxLayout()
#
#         text = QLabel("Group")
#         self.layout.addWidget(text)
#
#         self.setLayout(self.layout)


class Task(QWidget):

    def __init__(self):
        super().__init__()

        self.setAutoFillBackground(True)

        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.red)
        self.setPalette(p)

        self.setFixedHeight(50)

        self.layout = QHBoxLayout()

        text = QLabel("NEW TASK")
        self.layout.addWidget(text)

        self.setLayout(self.layout)


class TaskWidget(QWidget):

    def __init__(self):
        super().__init__()

        self.setAutoFillBackground(True)

        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.green)
        self.setPalette(p)

        self.layout = QVBoxLayout()

        self.setLayout(self.layout)

    def create_task(self):

        task = Task()
        self.layout.addWidget(task)


class TaskBar(QWidget):

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()

        # self.group = GroupWidget()
        self.task = TaskWidget()

        self.create_task = QPushButton("Создать задачу")
        self.create_task.clicked.connect(self.action_create_task)

        # self.layout.addWidget(self.group)
        self.layout.addWidget(self.task)
        self.layout.addWidget(self.create_task)

        self.setLayout(self.layout)

    def action_create_task(self):
        """ Создание новой задачи """

        self.task.create_task()

