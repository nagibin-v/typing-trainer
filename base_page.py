from PySide6 import QtWidgets as qtw, QtCore as qtc, QtGui as qtg
from __feature__ import snake_case, true_property

from constraints import sizes


class BasePage(qtw.QFrame):
    def __init__(self):
        super().__init__()
        self.line_width = 3
        self.set_fixed_size(qtc.QSize(sizes.PAGE_WIDTH, sizes.PAGE_HEIGHT))
        self.auto_fill_background = True
        self.set_frame_style(qtw.QFrame.Panel | qtw.QFrame.Raised)