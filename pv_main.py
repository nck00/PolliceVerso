from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6 import uic
import os
import sys

class PolliceVerso(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("pv.ui", self)
        self.initUi()
        # to be filled by the user
        self.posPics = []
        self.negPics = []
        self.listOfPics = []

    def initUi(self) -> None:
        self.actionSetup.triggered.connect(self.on_ActionSetup_triggered)
        self.actionJudge.triggered.connect(self.on_ActionJudge_triggered)
        self.actionAbout.triggered.connect(self.on_ActionAbout_triggered)
        self.statusbar.showMessage("File -> Setup to begin.")
        self.show()

    @pyqtSlot()
    def on_ActionSetup_triggered(self):
        """We use a couple of dialogs to ask the user:
        - Where are the pics? (folderPath: str)
        - Which filetypes? (suffixes: list)
        - Include subfolders? (recursive: bool)
        - What to do with positively judged pics? (pos2do: str)
        - What to do with negatively judged pics? (neg2do: str)
        If all questions are answered call getListOfPics
        TODO: Add suffix, recursive and judgement Dialogs
        """
        folderPath = QFileDialog.getExistingDirectory(self, "Select Folder")
        suffixes = (".jpg", ".gif", ".png")
        neg2do = "txt"
        pos2do = "txt"
        recursive = False
        if folderPath and recursive is not None:
            # TODO: Add dialog if listOfPics exists to ask if to extend or to replace
            self.listOfPics = self.getListOfPics(folderPath, recursive, suffixes)           

    @pyqtSlot()
    def on_ActionJudge_triggered(self):
        if not self.listOfPics:
            self.statusbar.showMessage("File -> Setup to begin!")
            return
        self.updatePic(0)

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
        if listOfPics: # atleast one image
            self.statusbar.showMessage(f"{len(listOfPics)} Pictures found in {folderPath}. File -> Judge to proceed.")
        else:
            self.statusbar.showMessage(f"{len(listOfPics)} Pictures found in {folderPath}.")
        return listOfPics

    @pyqtSlot()
    def on_ActionAbout_triggered(self):
        about = QDialog(self)
        about.setWindowTitle("About Pollice Verso")
        about.exec()

    @pyqtSlot()
    def on_posPushButton_clicked(self):
        pic = self.listOfPics.pop(0)
        self.posPics.append(pic)
        self.updatePic(0)

    @pyqtSlot()
    def on_negPushButton_clicked(self):
        pic = self.listOfPics.pop(0)
        self.negPics.append(pic)
        self.updatePic(0)

    def updatePic(self, picIndex = 0):
        """Changes to the next pic to judge for the user."""
        try:
            currentPic = self.listOfPics[picIndex]
            self.picLabel.setPixmap(QPixmap(currentPic).scaledToHeight(self.picLabel.size().height()))
        except IndexError: # no more pics!
            self.finish()

    def finish(self):
        """
        Get's called after all images where judged
        """
        for button in (self.posPushButton, self.negPushButton):
            button.setEnabled(False)
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PolliceVerso()
    window.showMaximized()
    app.exec()