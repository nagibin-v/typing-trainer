from PySide6 import QtWidgets as qtw, QtCore as qtc, QtGui as qtg
from __feature__ import snake_case, true_property

from collections.abc import Callable

from constraints import fonts


class BaseButton(qtw.QPushButton):
    def __init__(self, text: str, function: Callable[[], None], parent: qtw.QWidget = None):
        super().__init__(parent=parent)
        self.text = text
        self.font = fonts.BUTTON_FONT
        self.clicked.connect(function)
