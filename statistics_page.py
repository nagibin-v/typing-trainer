from PySide6 import QtWidgets as qtw, QtCore as qtc, QtGui as qtg
from __feature__ import snake_case, true_property

import math

from constraints import colors, fonts, statistics, texts
from statistics_calculator import StatisticsCalculator
from base_page import BasePage
from base_header import BaseHeader


class KeyDisplay(qtw.QLabel):
    def __init__(self, keys: str, par: qtw.QFrame, width=statistics.KEY_SIZE):
        super().__init__(parent=par)
        self.keys = keys
        self.cur_option = 0
        self.line_width = 3
        self.auto_fill_background = True
        self.set_frame_style(qtw.QFrame.Panel | qtw.QFrame.Raised)
        self.set_fixed_size(qtc.QSize(width, statistics.KEY_SIZE))
        self.font = fonts.KEY_FONT
        self.alignment = qtc.Qt.AlignmentFlag.AlignCenter
        self.update_text()

    def get_color(self) -> qtg.QColor:
        accuracy = StatisticsCalculator().get_accuracy(self.get_symbol())
        if accuracy == -1:
            self.tool_tip = f'No data'
            return colors.DARK_GRAY_COLOR
        self.tool_tip = f'Accuracy: {accuracy * 100:.0f}%'
        if accuracy >= statistics.GREEN_MIN_ACCURACY:
            return qtg.QColor(colors.GREEN_COLOR)
        if accuracy <= statistics.RED_MAX_ACCURACY:
            return qtg.QColor(colors.RED_COLOR)
        fraction = (accuracy - statistics.RED_MAX_ACCURACY) / \
                   (statistics.GREEN_MIN_ACCURACY - statistics.RED_MAX_ACCURACY)
        return qtg.QColor(math.ceil(fraction * colors.GREEN_COLOR_RGB[0] + (1 - fraction) * colors.RED_COLOR_RGB[0]),
                          math.ceil(fraction * colors.GREEN_COLOR_RGB[1] + (1 - fraction) * colors.RED_COLOR_RGB[1]),
                          math.ceil(fraction * colors.GREEN_COLOR_RGB[2] + (1 - fraction) * colors.RED_COLOR_RGB[2]))

    def get_text(self) -> str:
        if len(self.keys) == 2:
            return self.keys[self.cur_option]
        if self.keys == '\t':
            return "Tab"
        if self.keys == '\n':
            return "Enter"
        return "Space"

    def get_symbol(self) -> str:
        if len(self.keys) == 1:
            return self.keys
        return self.keys[self.cur_option]

    def switch_shift(self) -> None:
        self.cur_option = 1 - self.cur_option
        self.update_text()

    def set_color(self) -> None:
        palette = self.palette
        palette.set_color(self.background_role(), qtg.QColor(self.get_color()))
        self.palette = palette

    def update_text(self) -> None:
        self.text = self.get_text()
        self.set_color()


class StatisticsPage(BasePage):
    def __init__(self):
        super().__init__()
        layout = qtw.QVBoxLayout()
        layout.add_widget(BaseHeader(texts.STATISTICS_HEADER))
        layout.add_stretch()
        self.set_layout(layout)
        self.keys = []
        for keys, x_shift, y_shift in statistics.KEY_LOCATIONS:
            cur_key = KeyDisplay(keys, self)
            cur_key.move(x_shift, y_shift)
            self.keys.append(cur_key)
        enter_key = KeyDisplay('\n', self, statistics.LONG_KEY_SIZE)
        enter_key.move(*statistics.ENTER_LOCATION)
        tab_key = KeyDisplay('\t', self, statistics.LONG_KEY_SIZE)
        tab_key.move(*statistics.TAB_LOCATION)
        space_key = KeyDisplay(' ', self, statistics.SPACE_SIZE)
        space_key.move(*statistics.SPACE_LOCATION)
        self.make_shift_checkbox()

    def switch_shift(self) -> None:
        for key in self.keys:
            key.switch_shift()

    def make_shift_checkbox(self) -> None:
        shift_button = qtw.QPushButton(text='Shift', parent=self)
        shift_button.font = fonts.KEY_FONT
        shift_button.move(*statistics.SHIFT_BUTTON_LOCATION)
        shift_button.set_fixed_size(qtc.QSize(statistics.LONG_KEY_SIZE, statistics.KEY_SIZE))
        shift_button.pressed.connect(self.switch_shift)
