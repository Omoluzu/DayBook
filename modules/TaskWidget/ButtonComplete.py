#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Виджет непосредственно самой задачи
"""

from ico import recource

from PyQt5.QtWidgets import QPushButton

from wrapperQWidget5.WrapperWidget import wrapper_widget

__all__ = ['ButtonComplete']


class ButtonComplete(QPushButton):

    @wrapper_widget
    def __init__(self):
        super().__init__()

        self.config = {
            "size": 50,
            "flat": True,
            "icon": {
                "icon": "check.png",
                "resource": True,
                "size": 50
            }
        }
