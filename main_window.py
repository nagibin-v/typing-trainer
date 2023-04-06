from PySide6 import QtWidgets as qtw, QtCore as qtc
from __feature__ import snake_case, true_property
from enum import Enum
from functools import partial
from constraints import sizes, texts
from base_button import BaseButton
from main_window_actions import MainWindowActions
from typing_page import TypingPage
from main_menu_page import MainMenuPage
from levels_menu_page import LevelsMenuPage
from statistics_page import StatisticsPage
from upload_level_page import UploadLevelPage


class State(Enum):
    MAIN_MENU = 1
    LEVELS_MENU = 2
    RUN_LEVEL = 3
    STATISTICS = 4
    UPLOAD_LEVEL = 5


class MainWindow(qtw.QMainWindow):
    def __init__(self):
        super().__init__()
        self.window_title = texts.TITLE
        self.set_fixed_size(qtc.QSize(sizes.WINDOW_WIDTH, sizes.WINDOW_HEIGHT))
        self.state = State.MAIN_MENU
        self.level_to_load = None
        self.setup_main_window_actions()
        layout = qtw.QStackedLayout()
        self.container = qtw.QFrame(parent=self)
        self.container.set_fixed_size(qtc.QSize(sizes.WINDOW_WIDTH - 2 * sizes.WINDOW_WIDTH_BORDER,
                                                sizes.WINDOW_HEIGHT - 2 * sizes.WINDOW_HEIGHT_BORDER))
        self.container.set_layout(layout)
        self.container.move(sizes.WINDOW_WIDTH_BORDER, sizes.WINDOW_HEIGHT_BORDER)
        self.home_button = BaseButton(texts.HOME_BUTTON, MainWindowActions().home_function, parent=self)
        self.home_button.move(sizes.WINDOW_WIDTH - 2 * sizes.BUTTON_SIZE, 0)
        self.load_state()

    def setup_main_window_actions(self) -> None:
        actions = MainWindowActions()
        actions.home_function = partial(MainWindow.switch_to, self, State.MAIN_MENU)
        actions.levels_function = partial(MainWindow.switch_to, self, State.LEVELS_MENU)
        actions.statistics_function = partial(MainWindow.switch_to, self, State.STATISTICS)
        actions.upload_function = partial(MainWindow.switch_to, self, State.UPLOAD_LEVEL)
        actions.restart_function = partial(MainWindow.load_state, self)
        actions.level_run_function = partial(MainWindow.run_level, self)
        actions.next_level_function = partial(MainWindow.run_next_level, self)

    def make_widget_by_state(self) -> qtw.QWidget:
        if self.state == State.MAIN_MENU:
            return MainMenuPage()
        elif self.state == State.LEVELS_MENU:
            return LevelsMenuPage()
        elif self.state == State.RUN_LEVEL:
            return TypingPage(self.level_to_load)
        elif self.state == State.STATISTICS:
            return StatisticsPage()
        elif self.state == State.UPLOAD_LEVEL:
            return UploadLevelPage()
        else:
            # maybe should throw some exception
            pass

    def load_state(self) -> None:
        cur = self.make_widget_by_state()
        self.container.layout().add_widget(cur)
        self.container.layout().set_current_widget(cur)
        if self.state == State.MAIN_MENU:
            self.home_button.hide()
        else:
            self.home_button.show()

    def check_valid_level(self, file_path: str) -> bool:
        try:
            file = open(file_path, 'r')
        except FileNotFoundError or FileExistsError:
            return False
        lines = file.readlines()
        if len(lines) <= 2:
            return False
        second_line = lines[1].split()
        if len(second_line) != 2:
            return False
        try:
            goal_speed = int(second_line[0])
            goal_accuracy = float(second_line[1])
        except ValueError:
            return False
        if goal_speed < 0 or goal_speed > 500:
            return False
        if goal_accuracy < 0 or goal_accuracy > 1:
            return False
        return True

    def run_level(self, file_path: str) -> None:
        if not self.check_valid_level(file_path):
            message = qtw.QMessageBox()
            message.critical(self, 'Error', texts.ERROR_INVALID_FILE)
            return
        self.level_to_load = file_path
        self.switch_to(State.RUN_LEVEL)

    def run_next_level(self) -> None:
        if self.level_to_load[:len(texts.LEVEL_PATH_FIRST)] != texts.LEVEL_PATH_FIRST:
            return
        if self.level_to_load[-len(texts.LEVEL_PATH_LAST):] != texts.LEVEL_PATH_LAST:
            return
        cur_level_number = int(self.level_to_load[len(texts.LEVEL_PATH_FIRST):-len(texts.LEVEL_PATH_LAST)])
        next_level = texts.LEVEL_PATH_FIRST + f'{cur_level_number + 1:02d}' + texts.LEVEL_PATH_LAST
        self.run_level(next_level)

    def switch_to(self, new_state: State) -> None:
        self.state = new_state
        self.load_state()
