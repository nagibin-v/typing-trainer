from PySide6 import QtWidgets as qtw, QtCore as qtc, QtGui as qtg
from __feature__ import snake_case, true_property
from collections.abc import Callable

from base_button import BaseButton
from main_window_actions import MainWindowActions
from constraints import colors, fonts, texts


class MainMenuPage(qtw.QFrame):
    def __init__(self):
        super().__init__()
        layout = qtw.QVBoxLayout()
        layout.set_alignment(qtc.Qt.AlignmentFlag.AlignCenter)
        layout.add_stretch()
        layout.add_widget(self.make_logo())
        layout.add_widget(BaseButton(texts.LEVELS_BUTTON, MainWindowActions().levels_function))
        layout.add_widget(BaseButton(texts.STATISTICS_BUTTON, MainWindowActions().statistics_function))
        layout.add_widget(BaseButton(texts.UPLOAD_BUTTON, MainWindowActions().upload_function))
        layout.add_stretch()
        self.set_layout(layout)

    def make_logo(self) -> qtw.QLabel:
        logo = qtw.QLabel(text=texts.TITLE)
        logo.font = fonts.LOGO_FONT
        logo.set_style_sheet(f'color: {colors.GREEN_COLOR}')
        return logo
