from singleton import Singleton


class MainWindowActions(metaclass=Singleton):
    """
    The MainWindowActions is a singleton containing the page-switching functions
    """
    def __init__(self):
        self.next_level_function = None
        self.home_function = None
        self.levels_function = None
        self.statistics_function = None
        self.upload_function = None
        self.restart_function = None
        self.level_run_function = None
        self.next_level_function = None
