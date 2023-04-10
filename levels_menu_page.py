from PySide6 import QtWidgets as qtw, QtCore as qtc
from __feature__ import snake_case, true_property
from functools import partial

from constraints import colors, fonts, sizes, texts, level_list
from main_window_actions import MainWindowActions
from base_page import BasePage
from base_header import BaseHeader
from base_button import BaseButton


class BlockOfLevels(qtw.QFrame):
    """
    BlockOfLevels is a horizontal block of buttons to load levels, inherits QFrame

    Parameters:
        first (int), last(int): the range of the levels block contains, includes first, excludes last
    """
    def __init__(self, first: int, last: int):
        super().__init__()
        layout = qtw.QHBoxLayout()
        layout.set_alignment(qtc.Qt.AlignmentFlag.AlignLeft)
        for i in range(first, last):
            number_text = f'{i:02d}'
            button = BaseButton(number_text, partial(MainWindowActions().level_run_function,
                                                     texts.LEVEL_PATH_FIRST + number_text + texts.LEVEL_PATH_LAST))
            button.set_fixed_size(qtc.QSize(sizes.BUTTON_SIZE, sizes.BUTTON_SIZE))
            layout.add_widget(button)
        self.set_layout(layout)


class LevelsList(qtw.QFrame):
    """
    LevelsList is a list of all levels, inherits QFrame
    Does not take any parameters
    """
    def __init__(self):
        super().__init__()
        layout = qtw.QVBoxLayout()
        layout.set_alignment(qtc.Qt.AlignmentFlag.AlignVCenter)
        for name, first, last in level_list.LEVEL_LIST:
            self.add_group_of_levels(layout, name, first, last)
        self.set_layout(layout)

    @staticmethod
    def add_group_of_levels(layout: qtw.QLayout, title: str, first: int, last: int) -> None:
        title_label = qtw.QLabel(text=title)
        title_label.font = fonts.HEADER_FONT
        title_label.set_style_sheet(f'color: {colors.GREEN_COLOR}')
        layout.add_widget(title_label)
        layout.add_widget(BlockOfLevels(first, last))


class LevelsMenuPage(BasePage):
    """
    LevelsMenuPage is a page for level selection menu, inherits BasePage
    Does not take any parameters
    """
    def __init__(self):
        super().__init__()
        layout = qtw.QVBoxLayout()
        layout.set_alignment(qtc.Qt.AlignmentFlag.AlignVCenter)
        layout.add_widget(BaseHeader(texts.LEVELS_HEADER))
        scroll = qtw.QScrollArea()
        scroll.set_widget(LevelsList())
        layout.add_widget(scroll)
        self.set_layout(layout)
