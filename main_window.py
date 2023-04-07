from PySide6 import QtWidgets as qtw, QtCore as qtc
from __feature__ import snake_case, true_property
from enum import Enum
from functools import partial
from constraints import sizes, texts
from base_button import BaseButton
from base_page import BasePage
from main_window_actions import MainWindowActions
from typing_page import TypingPage
from main_menu_page import MainMenuPage
from levels_menu_page import LevelsMenuPage
from statistics_page import StatisticsPage
from upload_level_page import UploadLevelPage
from level_validator import LevelValidator


class State(Enum):
    """
    State is an Enum representing the current page shown
    """
    MAIN_MENU = 1
    LEVELS_MENU = 2
    RUN_LEVEL = 3
    STATISTICS = 4
    UPLOAD_LEVEL = 5


class MainWindow(qtw.QMainWindow):
    """
    MainWindow is the main window of the app, inherits QMainWindow
    Does not take any parameters
    Attributes:
        state (State): current state
        container (QFrame): widget containing current page
        home_button (BaseButton): button to go to main page
    """
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
        """
        Sets up the MainWindowActions()'s functions which are called from MainWindow object
        """
        actions = MainWindowActions()
        actions.home_function = partial(MainWindow.switch_to, self, State.MAIN_MENU)
        actions.levels_function = partial(MainWindow.switch_to, self, State.LEVELS_MENU)
        actions.statistics_function = partial(MainWindow.switch_to, self, State.STATISTICS)
        actions.upload_function = partial(MainWindow.switch_to, self, State.UPLOAD_LEVEL)
        actions.restart_function = partial(MainWindow.load_state, self)
        actions.level_run_function = partial(MainWindow.run_level, self)
        actions.next_level_function = partial(MainWindow.run_next_level, self)

    def make_page_by_state(self) -> BasePage:
        """
        Creates a page by current state
        Raises:
            ValueError: not correct state
        Returns:
            page (BasePage), an instance of a necessary page
        """
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
            raise ValueError("MainWindow.state should be one of the State options")

    def load_state(self) -> None:
        """
        Reloads current page, shows or hides home button
        """
        cur = self.make_page_by_state()
        self.container.layout().add_widget(cur)
        self.container.layout().set_current_widget(cur)
        if self.state == State.MAIN_MENU:
            self.home_button.hide()
        else:
            self.home_button.show()

    def run_level(self, file_path: str) -> None:
        """
        Switches page to level page and runs level located at file_path
        Parameters:
            file_path (str): path to file to load
        In case file_path is incorrect, shows message box
        """
        if not LevelValidator.is_level_valid(file_path):
            message = qtw.QMessageBox()
            message.critical(self, 'Error', texts.ERROR_INVALID_FILE)
            return
        self.level_to_load = file_path
        self.switch_to(State.RUN_LEVEL)

    def run_next_level(self) -> None:
        """
        Loads the next level
        In case current level is not one of the pre-made levels, does nothing
        """
        if self.level_to_load[:len(texts.LEVEL_PATH_FIRST)] != texts.LEVEL_PATH_FIRST:
            return
        if self.level_to_load[-len(texts.LEVEL_PATH_LAST):] != texts.LEVEL_PATH_LAST:
            return
        cur_level_number = int(self.level_to_load[len(texts.LEVEL_PATH_FIRST):-len(texts.LEVEL_PATH_LAST)])
        next_level = texts.LEVEL_PATH_FIRST + f'{cur_level_number + 1:02d}' + texts.LEVEL_PATH_LAST
        self.run_level(next_level)

    def switch_to(self, new_state: State) -> None:
        """
        Switches state to new_state, loads the page
        Parameters:
            new_state (State): new state
        """
        self.state = new_state
        self.load_state()
