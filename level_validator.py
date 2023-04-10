from singleton import Singleton


class LevelValidator(metaclass=Singleton):
    """
    LevelValidator checks that text file is a valid level
    """
    @staticmethod
    def is_level_valid(file_path: str) -> bool:
        try:
            file = open(file_path, 'r')
        except (FileNotFoundError, FileExistsError):
            return False
        lines = file.readlines()
        if len(lines) <= 2:
            return False
        second_line = lines[1].split()
        if len(second_line) != 2:
            return False
        try:
            goal_speed = float(second_line[0])
            goal_accuracy = float(second_line[1])
        except ValueError:
            return False
        if goal_speed < 0 or goal_speed > 500:
            return False
        if goal_accuracy < 0 or goal_accuracy > 1:
            return False
        return True
