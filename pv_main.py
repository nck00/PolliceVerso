from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6 import uic
import os
import sys

class PolliceVerso(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("pv.ui", self)
        self.initUi()

    def initUi(self) -> None:
        self.actionSetup.triggered.connect(self.on_ActionSetup_triggered)
        self.actionAbout.triggered.connect(self.on_ActionAbout_triggered)
        self.show()

    @pyqtSlot()
    def on_ActionSetup_triggered(self):
        """We use a couple of dialogs to ask the user:
        - Where are the pics? (folderPath: str)
        - Which filetypes? (suffixes: list)
        - Include subfolders? (recursive: bool)
        If all questions are answered call getListOfPics
        TODO: Add suffix and recursive Dialogs
        """
        folderPath = QFileDialog.getExistingDirectory(self, "Select Folder")
        suffixes = (".jpg", ".gif", ".png")
        recursive = False
        if folderPath and recursive is not None:
            self.getListOfPics(folderPath, recursive, suffixes)           

    @pyqtSlot()
    def on_ActionAbout_triggered(self):
        about = QDialog(self)
        about.setWindowTitle("About Pollice Verso")
        about.exec()

    def getListOfPics(self, folderPath: str, recursive: bool, suffixes: list) -> list:
        """
        Returns a list of all files of the selected filetypes in the selected folder
        (and subfolder if recursive is True)
        """
        listOfPics = []
        with os.scandir(folderPath) as path:
            for entry in path:
                if entry.is_file() and os.path.splitext(entry)[1] in suffixes:
                    listOfPics.append(os.path.normpath(entry.path))
        return listOfPics

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