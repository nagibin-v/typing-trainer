from PySide6 import QtWidgets as qtw, QtCore as qtc, QtGui as qtg
from __feature__ import snake_case, true_property

import math

from constraints import colors, fonts, statistics, texts
from statistics_calculator import StatisticsCalculator
from base_page import BasePage
from base_header import BaseHeader


class KeyDisplay(qtw.QLabel):
    """
    KeyDisplay is an interface object showing the accuracy of types of a key via color, inherits QLabel

    Parameters:
        symbols (str): two symbols key represents: without shift pressed and with shift pressed,
                       in case they are the same, only one symbol
        par (qtw.QFrame): parent widget
        width (int): the width of a key, same as height by default

    Attributes:
        symbols (str): the symbols key represents
        cur_option (int): 0 if shift it shows key without shift pressed, 1 otherwise
    """
    def __init__(self, symbols: str, par: qtw.QFrame, width: int = statistics.KEY_SIZE):
        super().__init__(parent=par)
        self.symbols = symbols
        self.cur_option = 0
        self.line_width = 3
        self.auto_fill_background = True
        self.set_frame_style(qtw.QFrame.Panel | qtw.QFrame.Raised)
        self.set_fixed_size(qtc.QSize(width, statistics.KEY_SIZE))
        self.font = fonts.KEY_FONT
        self.alignment = qtc.Qt.AlignmentFlag.AlignCenter
        self.update_view()

    def get_accuracy(self) -> float:
        """
        Returns the accuracy of current symbol of the key
        Returns:
            accuracy (float)
        """
        return StatisticsCalculator().get_accuracy(self.get_symbol())

    def setup_tool_tip(self) -> None:
        """
        Sets up the tool tip for the key
        """
        accuracy = self.get_accuracy()
        if accuracy == -1:
            self.tool_tip = f'<font color=black>{texts.NO_DATA_TEXT}</font>'
        else:
            self.tool_tip = f'<Font color=black>{texts.ACCURACY_TEXT}: {accuracy * 100:.0f}%</font>'

    def get_color(self) -> qtg.QColor:
        """
        Returns the color of the key calculated by its current symbol accuracy
        Returns:
            color (QColor)
        """
        accuracy = self.get_accuracy()
        if accuracy == -1:
            return colors.DARK_GRAY_COLOR
        if accuracy >= statistics.GREEN_MIN_ACCURACY:
            return qtg.QColor(colors.GREEN_COLOR)
        if accuracy <= statistics.RED_MAX_ACCURACY:
            return qtg.QColor(colors.RED_COLOR)
        fraction = ((accuracy - statistics.RED_MAX_ACCURACY) /
                    (statistics.GREEN_MIN_ACCURACY - statistics.RED_MAX_ACCURACY))
        return qtg.QColor(math.ceil(fraction * colors.GREEN_COLOR_RGB[0] + (1 - fraction) * colors.RED_COLOR_RGB[0]),
                          math.ceil(fraction * colors.GREEN_COLOR_RGB[1] + (1 - fraction) * colors.RED_COLOR_RGB[1]),
                          math.ceil(fraction * colors.GREEN_COLOR_RGB[2] + (1 - fraction) * colors.RED_COLOR_RGB[2]))

    def get_text(self) -> str:
        """
        Returns the text that should be shown on the key
        It is different from the symbol for Space, Tab and Enter keys
        Returns:
            text (str)
        """
        if len(self.symbols) == 2:
            return self.symbols[self.cur_option]
        if self.symbols == '\t':
            return "Tab"
        if self.symbols == '\n':
            return "Enter"
        return "Space"

    def get_symbol(self) -> str:
        """
        Returns the current symbol depending on cur_option
        Returns:
            symbol (str)
        """
        if len(self.symbols) == 1:
            return self.symbols
        return self.symbols[self.cur_option]

    def switch_shift(self) -> None:
        """
        Switches the key state when shift state changes
        """
        self.cur_option = 1 - self.cur_option
        self.update_view()

    def set_color(self) -> None:
        """
        Sets up the color of the key
        """
        palette = self.palette
        palette.set_color(self.background_role(), qtg.QColor(self.get_color()))
        self.palette = palette

    def update_view(self) -> None:
        """
        Updates the look of the key: text, color and tool tip
        """
        self.text = self.get_text()
        self.set_color()
        self.setup_tool_tip()


class StatisticsPage(BasePage):
    """
    StatisticPage is a page where the accuracy statistics for each key is shown
    Does not take any parameters
    """
    def __init__(self):
        super().__init__()
        layout = qtw.QVBoxLayout()
        layout.add_widget(BaseHeader(texts.STATISTICS_HEADER))
        layout.add_stretch()
        self.set_layout(layout)
        self.keys = []
        for symbols, x_shift, y_shift in statistics.KEY_LOCATIONS:
            cur_key = KeyDisplay(symbols, self)
            cur_key.move(x_shift, y_shift)
            self.keys.append(cur_key)
        enter_key = KeyDisplay('\n', self, statistics.LONG_KEY_SIZE)
        enter_key.move(*statistics.ENTER_LOCATION)
        tab_key = KeyDisplay('\t', self, statistics.LONG_KEY_SIZE)
        tab_key.move(*statistics.TAB_LOCATION)
        space_key = KeyDisplay(' ', self, statistics.SPACE_SIZE)
        space_key.move(*statistics.SPACE_LOCATION)
        self.make_shift_button()

    def switch_shift(self) -> None:
        """
        Switches the state of all the keys when shift state is changed
        """
        for key in self.keys:
            key.switch_shift()

    def make_shift_button(self) -> None:
        """
        Creates the button to switch state of all the keys via shift
        """
        shift_button = qtw.QPushButton(text='Shift', parent=self)
        shift_button.font = fonts.KEY_FONT
        shift_button.move(*statistics.SHIFT_BUTTON_LOCATION)
        shift_button.set_fixed_size(qtc.QSize(statistics.LONG_KEY_SIZE, statistics.KEY_SIZE))
        shift_button.pressed.connect(self.switch_shift)
