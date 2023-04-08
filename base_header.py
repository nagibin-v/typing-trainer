from PySide6 import QtWidgets as qtw, QtCore as qtc, QtGui as qtg
from __feature__ import snake_case, true_property

from constraints import fonts, colors


class BaseHeader(qtw.QLabel):
    """
    BaseHeader is a standard header used in the interface, inherits QLabel

    Parameters:
        text (str): the title of the header
    """
    def __init__(self, text: str):
        super().__init__()
        self.font = fonts.HEADER_FONT
        self.set_style_sheet(f'color: {colors.WHITE_COLOR}')
        self.text = '<b>' + text + '<\b>'
        self.alignment = qtc.Qt.AlignmentFlag.AlignCenter
