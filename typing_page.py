from PySide6 import QtWidgets as qtw, QtCore as qtc
from __feature__ import snake_case, true_property

import html
import time
import math
from collections import Counter

from main_window_actions import MainWindowActions
from constraints import colors, fonts, sizes, texts
from statistics_calculator import StatisticsCalculator
from base_page import BasePage
from base_button import BaseButton
from base_header import BaseHeader


class Typer(qtw.QTextEdit):
    """
    Typer is a widget where the user types the text and sees the text to type, inherits QTextEdit
    Also it collects the information about types, namely speed and accuracy

    Parameters:
        text (str): text to type
        goal_speed (float): speed user should have to get maximal score
        goal_accuracy (float): accuracy user should have to get maximal score
        status_bar (QStatusBar): status bar to write current speed

    Attributes:
        typing_text (str): the text to type
        goal_speed (float)
        goal_accuracy (float)
        progress (int): the number of symbols typed correctly
        start_time_stamp (float): the moment of the start of typing
        mistakes_counter (Counter[str, int]): Counter counting mistakes
    """
    def __init__(self, text: str, goal_speed: float, goal_accuracy: float, status_bar: qtw.QStatusBar):
        super().__init__()
        self.typing_text = text
        self.goal_speed = goal_speed
        self.goal_accuracy = goal_accuracy
        self.progress = 0
        self.update_text()
        self.start_time_stamp = None
        self.status_bar = status_bar
        self.mistakes_counter = Counter()

    @staticmethod
    def format_text_to_html(text: str, color: str) -> str:
        """
        Formats text to html so that all symbols are displayed right and colored in color
        Parameters:
            text (str): text to format
            color (str): color of text #RRGGBB
        Returns:
            line (str): formatted text
        """
        return f'<t style="color: {color};white-space:pre-wrap">' + \
            html.escape(text).replace('\n', '↵<br />').replace('\t', ' ⇥ ') + '</t>'

    def move_cursor_to_place(self) -> None:
        """
        Moves the cursor after the symbols typed correctly
        """
        cur_cursor = self.text_cursor()
        cur_cursor.set_position(self.progress + self.typing_text[:self.progress].count('\n') +
                                self.typing_text[:self.progress].count('\t') * 2)
        self.set_text_cursor(cur_cursor)

    def update_text(self) -> None:
        """
        Updates the displayed text so the color of typed is green and the color of the rest is gray, moves the cursor
        """
        self.font = fonts.TYPER_FONT
        self.html = (self.format_text_to_html(self.typing_text[:self.progress], colors.GREEN_COLOR) +
                     self.format_text_to_html(self.typing_text[self.progress:], colors.GRAY_COLOR))
        self.move_cursor_to_place()

    def update_status(self) -> None:
        """
        Shows status bar message with speed
        """
        self.status_bar.show_message(f'{texts.SPEED_TEXT}: {self.get_speed():.2f} {texts.SPEED_RESOLUTION}', 500)

    def key_press_event(self, event) -> None:
        """
        Overloaded virtual function, calls type with the typed symbol
        """
        if self.progress == len(self.typing_text):
            return
        symbol = event.text()
        if self.start_time_stamp is None:
            self.start_time_stamp = time.time_ns()
        if event.key() == qtc.Qt.Key_Enter or event.key() == qtc.Qt.Key_Return:  # enter or numpad enter
            symbol = '\n'
        if symbol == "":
            return
        self.type(symbol)

    def type(self, symbol: str) -> None:
        """
        Does staff when symbol is typed, recolors text if it is correct and counts the mistake otherwise
        Parameters:
            symbol (str): symbol typed
        """
        need = self.typing_text[self.progress]
        if need == symbol:
            self.progress += 1
            self.update_text()
            self.update_status()
            if self.progress == len(self.typing_text):
                self.finish_level()
        else:
            self.mistakes_counter[need] += 1

    def get_speed(self) -> float:
        """
        Return current speed in Words Per Minute
        Returns:
            speed (float)
        """
        cur_time = (time.time_ns() - self.start_time_stamp) / 10 ** 9 / 60  # in minutes
        cur_word_count = self.progress / 5  # in words
        return cur_word_count / cur_time

    def get_accuracy(self) -> float:
        """
        Return current accuracy, the share of symbols typed correctly
        Returns:
            accuracy (float)
        """
        all_cnt = self.progress + self.mistakes_counter.total()
        return self.progress / all_cnt

    def finish_level(self) -> None:
        """
        Finishes level, updates the statistics and shows the level end widget
        """
        StatisticsCalculator().add_stats(self.mistakes_counter, Counter(self.typing_text))
        self.set_layout(FinishLayout(self.get_speed(), self.goal_speed, self.get_accuracy(), self.goal_accuracy))

    # overloaded functions for user not to be able to do anything on Typer with mouse
    def mouse_press_event(self, event):
        pass

    def mouse_double_click_event(self, event):
        pass


class FinishLayout(qtw.QVBoxLayout):
    """
    FinishLayout is a layout of interface when level is finished, inherits QVBoxLayout
    Parameters:
        speed (float): user's speed
        goal_speed (float): level goal speed
        accuracy (float): user's accuracy
        goal_accuracy (float): level goal accuracy
    """
    def __init__(self, speed: float, goal_speed: float, accuracy: float, goal_accuracy: float):
        super().__init__()
        self.set_alignment(qtc.Qt.AlignmentFlag.AlignCenter)
        self.add_stretch()
        self.add_widget(self.make_score_widget(speed, goal_speed, accuracy, goal_accuracy))
        self.add_widget(self.make_buttons())
        self.add_stretch()

    @staticmethod
    def get_score(speed: float, goal_speed: float, accuracy: float, goal_accuracy: float) -> int:
        """
        Calculates the score of user based on his speed and accuracy.
        The score is an integer from 0 to 5000
        Parameters:
            speed (float): user's speed
            goal_speed (float): level goal speed
            accuracy (float): user's accuracy
            goal_accuracy (float): level goal accuracy
        Returns:
            score (int)
        """
        return math.ceil(min(speed, goal_speed) / goal_speed * 2500 +
                         min(accuracy, goal_accuracy) / goal_accuracy * 2500)

    def make_score_widget(self, speed: float, goal_speed: float, accuracy: float, goal_accuracy: float) -> qtw.QFrame:
        """
        Creates a widget showing score, speed and accuracy
        Parameters:
            speed (float): user's speed
            goal_speed (float): level goal speed
            accuracy (float): user's accuracy
            goal_accuracy (float): level goal accuracy
        Returns:
            score_widget (QFrame)
        """
        score_widget = qtw.QFrame()
        score_widget.line_width = 3
        score_widget.set_frame_style(qtw.QFrame.Panel | qtw.QFrame.Raised)
        score_widget.auto_fill_background = True
        score_widget.set_fixed_size(qtc.QSize(sizes.SCORE_WINDOW_WIDTH, sizes.SCORE_WINDOW_HEIGHT))
        layout = qtw.QVBoxLayout()
        layout.set_alignment(qtc.Qt.AlignmentFlag.AlignCenter)
        score_text = qtw.QLabel(text=f'{self.get_score(speed, goal_speed, accuracy, goal_accuracy)}')
        score_text.font = fonts.TYPER_SCORE_FONT
        score_text.set_style_sheet(f'color: {colors.GREEN_COLOR}')
        layout.add_stretch()
        layout.add_widget(score_text)
        layout.add_stretch()
        stats_text = qtw.QLabel(text=f'{texts.SPEED_TEXT}: {speed:.2f} {texts.SPEED_RESOLUTION}   ' +
                                     f'{texts.ACCURACY_TEXT}: {accuracy * 100:.0f}{texts.ACCURACY_RESOLUTION}')
        stats_text.font = fonts.TYPER_STATISTICS_FONT
        layout.add_widget(stats_text)
        score_widget.set_layout(layout)
        return score_widget

    @staticmethod
    def make_buttons() -> qtw.QFrame:
        """
        Creates the buttons to main menu, restart and next level
        Returns:
            buttons (QFrame)
        """
        buttons = qtw.QFrame()
        buttons.set_fixed_size(qtc.QSize(sizes.SCORE_WINDOW_WIDTH, sizes.BUTTON_SIZE))
        layout = qtw.QHBoxLayout()
        layout.add_widget(BaseButton(texts.HOME_BUTTON, MainWindowActions().home_function))
        layout.add_widget(BaseButton(texts.RESTART_BUTTON, MainWindowActions().restart_function))
        layout.add_widget(BaseButton(texts.NEXT_BUTTON, MainWindowActions().next_level_function))
        buttons.set_layout(layout)
        return buttons


class TypingSpeedometer(qtw.QStatusBar):
    """
    TypingSpeedometer is a status bar to show current speed, inherits QStatusBar
    Does not take any parameters
    """
    def __init__(self):
        super().__init__()
        self.font = fonts.TYPER_STATUS_BAR_FONT


class TypingPage(BasePage):
    """
    TypingPage is a page where user completes the level

    Parameters:
        file_path (str): path to file with level
    """
    def __init__(self, file_path: str):
        super().__init__()
        with open(file_path, 'r') as file:
            all_lines = file.readlines()
        header = all_lines[0]
        goal_speed, goal_accuracy = map(float, all_lines[1].split())
        text = ''.join(all_lines[2:])
        layout = qtw.QVBoxLayout()
        layout.add_widget(BaseHeader(header))
        status_bar = qtw.QStatusBar()
        layout.add_widget(Typer(text, goal_speed, goal_accuracy, status_bar))
        layout.add_widget(status_bar)
        self.set_layout(layout)
