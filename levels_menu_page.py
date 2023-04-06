from PySide6 import QtWidgets as qtw, QtCore as qtc
from __feature__ import snake_case, true_property
from functools import partial

from constraints import colors, fonts, sizes, texts
from main_window_actions import MainWindowActions
from base_page import BasePage
from base_header import BaseHeader


class LevelBox(qtw.QFrame):
    def __init__(self, first: int, last: int):
        super().__init__()
        layout = qtw.QHBoxLayout()
        layout.set_alignment(qtc.Qt.AlignmentFlag.AlignLeft)
        for i in range(first, last):
            number_text = f'{i:02d}'
            button = qtw.QPushButton(number_text)
            button.font = fonts.BUTTON_FONT
            button.clicked.connect(partial(MainWindowActions().level_run_function,
                                           texts.LEVEL_PATH_FIRST + number_text + texts.LEVEL_PATH_LAST))
            button.set_fixed_size(qtc.QSize(sizes.BUTTON_SIZE, sizes.BUTTON_SIZE))
            layout.add_widget(button)
        self.set_layout(layout)


class LevelsMenuPage(BasePage):
    def __init__(self):
        super().__init__()
        layout = qtw.QVBoxLayout()
        layout.set_alignment(qtc.Qt.AlignmentFlag.AlignVCenter)
        layout.add_widget(BaseHeader(texts.LEVELS_HEADER))
        layout.add_stretch()
        # layout.add_stretch()
        self.add_group_of_levels(layout, 'Introduction', 0, 1)
        self.add_group_of_levels(layout, 'English Letters', 1, 10)
        self.add_group_of_levels(layout, 'Extra', 10, 20)
        # layout.add_stretch()
        self.set_layout(layout)

    def add_group_of_levels(self, layout: qtw.QLayout, title: str, first: int, last: int) -> None:
        title_label = qtw.QLabel(text=title)
        title_label.font = fonts.HEADER_FONT
        title_label.set_style_sheet(f'color: {colors.GREEN_COLOR}')
        layout.add_widget(title_label)
        layout.add_widget(LevelBox(first, last))
