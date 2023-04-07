from PySide6 import QtWidgets as qtw, QtCore as qtc
from __feature__ import snake_case, true_property

from constraints import sizes


class BasePage(qtw.QFrame):
    """
    BasePage is the base class for pages of app, inherits QFrame
    It sets up the standard design of a page, takes no parameters
    """
    def __init__(self):
        super().__init__()
        self.line_width = 3
        self.set_fixed_size(qtc.QSize(sizes.PAGE_WIDTH, sizes.PAGE_HEIGHT))
        self.auto_fill_background = True
        self.set_frame_style(qtw.QFrame.Panel | qtw.QFrame.Raised)
