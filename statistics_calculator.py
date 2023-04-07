from singleton import Singleton
import pickle
from collections import Counter
from constraints import texts


class StatisticsCalculator(metaclass=Singleton):
    def __init__(self):
        self.mistakes_counter = Counter()
        self.letter_counter = Counter()
        self.load_stats_file()

    def add_stats(self, mistakes_counter: Counter[str, int], letter_counter: Counter[str, int]):
        self.mistakes_counter += mistakes_counter
        self.letter_counter += letter_counter
        self.update_stats_file()

    def load_stats_file(self) -> None:
        with open(texts.STATISTICS_PATH, 'rb') as file:
            try:
                data = pickle.load(file)
                self.mistakes_counter = data[0]
                self.letter_counter = data[1]
            except:
                self.mistakes_counter = Counter()
                self.letter_counter = Counter()

    def update_stats_file(self) -> None:
        with open(texts.STATISTICS_PATH, 'wb') as file:
            pickle.dump((self.mistakes_counter, self.letter_counter), file)

    def get_accuracy(self, symbol: str) -> float:
        if symbol not in self.letter_counter:
            return -1
        all_cnt = self.letter_counter[symbol] + self.mistakes_counter[symbol]
        return self.letter_counter[symbol] / all_cnt
