from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6 import uic
import sys

class PolliceVerso(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("pv.ui", self)
        self.show()

    @pyqtSlot()
    def on_posPushButton_clicked(self):
        print("positive")

    @pyqtSlot()
    def on_negPushButton_clicked(self):
        print("negative")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PolliceVerso()
    window.showMaximized()
    app.exec()