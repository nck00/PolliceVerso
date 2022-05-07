from PyQt6.QtWidgets import *
from PyQt6 import uic

class ToDoDialog(QDialog):
    def __init__(self, choice: str):
        super().__init__()
        uic.loadUi("pv_toDo.ui", self)
        self.setWindowTitle(f"What should happen with {choice} evaluated images?")
        self.show()

class suffixesDialog(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("pv_suffixes.ui", self)
        self.show()