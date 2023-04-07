from PySide6 import QtWidgets as qtw, QtCore as qtc, QtGui as qtg
from __feature__ import snake_case, true_property
from constraints import fonts, texts
from base_page import BasePage
from base_header import BaseHeader
from base_button import BaseButton
from main_window_actions import MainWindowActions


class Instruction(qtw.QTextBrowser):
    def __init__(self):
        super().__init__()
        with open(texts.INSTRUCTION_PATH, 'r') as file:
            self.html = file.read()
        self.font = fonts.TYPER_FONT
        self.alignment = qtc.Qt.AlignmentFlag.AlignCenter


class UploadLevelPage(BasePage):
    def __init__(self):
        super().__init__()
        layout = qtw.QVBoxLayout()
        layout.add_widget(BaseHeader(texts.UPLOAD_HEADER))
        layout.add_widget(Instruction())
        layout.add_widget(BaseButton(texts.UPLOAD_BUTTON, self.load_level))
        self.set_layout(layout)

    def load_level(self) -> None:
        file_name = qtw.QFileDialog.get_open_file_name(self, filter='Text (*.txt)')[0]
        MainWindowActions().level_run_function(file_name)
