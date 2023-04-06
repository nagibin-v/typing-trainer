from PySide6 import QtWidgets as qtw, QtCore as qtc
from __feature__ import snake_case, true_property
import sys
from main_window import MainWindow


def main():
    app = qtw.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()


if __name__ == '__main__':
    main()
