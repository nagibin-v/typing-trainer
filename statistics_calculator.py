from singleton import Singleton
import pickle
from collections import Counter
from constraints import texts


class StatisticsCalculator(metaclass=Singleton):
    """
    StatisticsCalculator is a singleton collecting statistics about right and wrong types of each symbol
    It stores data in texts.STATISTICS_PATH with pickle
    Does not take any parameters

    Attributes:
        mistakes_counter (Counter[str, int]): Counter with number of mistakes made for each symbol
        letter_counter (Counter[str, int]): Counter with number of correct types made for each symbol
    """
    def __init__(self):
        self.mistakes_counter = Counter()
        self.letter_counter = Counter()
        self.load_stats_file()

    def add_stats(self, mistakes_counter: Counter[str, int], letter_counter: Counter[str, int]) -> None:
        """
        Adds up the information about types, updates the saves file
        Parameters:
            mistakes_counter (Counter[str, int]): Counter with number of mistakes made for each symbol
            letter_counter (Counter[str, int]): Counter with number of right types of each symbol
        """
        self.mistakes_counter += mistakes_counter
        self.letter_counter += letter_counter
        self.update_stats_file()

    def load_stats_file(self) -> None:
        """
        Loads the information from saves file
        """
        with open(texts.STATISTICS_PATH, 'rb') as file:
            try:
                data = pickle.load(file)
                self.mistakes_counter = data[0]
                self.letter_counter = data[1]
            except (AttributeError, EOFError, ImportError, IndexError):  # in case file was broken or empty
                self.mistakes_counter = Counter()
                self.letter_counter = Counter()

    def update_stats_file(self) -> None:
        """
        Updates the information in saves file
        """
        with open(texts.STATISTICS_PATH, 'wb') as file:
            pickle.dump((self.mistakes_counter, self.letter_counter), file)

    def get_accuracy(self, symbol: str) -> float:
        """
        Returns the accuracy - fraction of right types of a symbol
        Parameters:
            symbol (str): symbol for accuracy calculation
        In case the symbol was never typed, returns -1
        """
        if symbol not in self.letter_counter:
            return -1
        all_cnt = self.letter_counter[symbol] + self.mistakes_counter[symbol]
        return self.letter_counter[symbol] / all_cnt
