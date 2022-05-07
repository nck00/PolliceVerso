from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6 import uic
import os
import sys
from pv_dialogs import *

class PolliceVerso(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("pv.ui", self)
        self.initUi()
        # to be filled by the user
        self.posPics = []
        self.negPics = []
        self.listOfPics = []
        self.lastPic = ""

    def initUi(self) -> None:
        self.actionSetup.triggered.connect(self.on_ActionSetup_triggered)
        self.actionJudge.triggered.connect(self.on_ActionJudge_triggered)
        self.actionUndo.triggered.connect(self.on_ActionUndo_triggered)
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
        suffixes = self.askSuffixes()
        self.neg2do = self.askToDo("negative")
        self.pos2do = self.askToDo("positive")
        recursive = self.askRecursive()
        if folderPath and recursive is not None:
            # TODO: Add dialog if listOfPics exists to ask if to extend or to replace
            self.listOfPics = self.getListOfPics(folderPath, recursive, suffixes)

    def askSuffixes(self) -> list:
        suffixes = suffixesDialog()
        suffixes.exec()
        return (".jpg", ".gif", ".png", ".webp")

    def askToDo(self, choice: str) -> str:
        toDo = ToDoDialog(choice)
        toDo.exec()
        return toDo.choiceComboBox.currentText()

    def askRecursive(self):
        recursiveQuestion = QMessageBox()
        recursiveQuestion.setWindowTitle("Recursive?")
        recursiveQuestion.setText("Scan directories recursively?")
        recursiveQuestion.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        answer = recursiveQuestion.exec()
        if answer == QMessageBox.StandardButton.Yes:
            return True
        elif answer == QMessageBox.StandardButton.No:
            return False

    @pyqtSlot()
    def on_ActionJudge_triggered(self):
        if not self.listOfPics:
            self.statusbar.showMessage("File -> Setup to begin!")
            return
        for button in (self.posPushButton, self.negPushButton):
            button.setEnabled(True)
        self.updatePic(0)

    def getListOfPics(self, folderPath: str, recursive: bool, suffixes: list) -> list:
        """
        Returns a list of all files of the selected filetypes in the selected folder
        (and subfolder if recursive is True)
        """
        listOfPics = []
        if recursive:
            listOfPics = [os.path.normpath(os.path.join(dp, f)) for dp, dn, files in os.walk(folderPath) for f in files if os.path.splitext(f)[1].lower() in suffixes]
        else:
            with os.scandir(folderPath) as path:
                for entry in path:
                    if entry.is_file() and os.path.splitext(entry)[1].lower() in suffixes:
                        listOfPics.append(os.path.normpath(entry.path))
        if listOfPics: # atleast one image
            self.statusbar.showMessage(f"{len(listOfPics)} Pictures found in {folderPath}. File -> Judge to proceed.")
        else:
            self.statusbar.showMessage(f"{len(listOfPics)} Pictures found in {folderPath}.")
        return listOfPics

    @pyqtSlot()
    def on_ActionUndo_triggered(self):
        """Undoes the last judgment and adds the pic into the listOfPics again.
        """
        if self.negPics and self.lastPic == self.negPics[-1]:
            pic = self.negPics.pop()
        elif self.posPics and self.lastPic == self.posPics[-1]:
            pic = self.posPics.pop()
        else: # None yet selected (lastPic == "")
            return 
        self.listOfPics.insert(1, pic)
        self.lastPic = ""

    @pyqtSlot()
    def on_ActionAbout_triggered(self):
        about = QDialog(self)
        about.setWindowTitle("About Pollice Verso")
        aboutLayout = QVBoxLayout()
        aboutLabel = QLabel(about)
        aboutLabel.setText("Pollice Verso is an easy way to sort pictures.")
        aboutLayout.addWidget(aboutLabel)
        about.setLayout(aboutLayout)
        about.exec()

    @pyqtSlot()
    def on_posPushButton_clicked(self):
        pic = self.listOfPics.pop(0)
        self.posPics.append(pic)
        self.lastPic = pic
        self.updatePic(0)

    @pyqtSlot()
    def on_negPushButton_clicked(self):
        pic = self.listOfPics.pop(0)
        self.negPics.append(pic)
        self.lastPic = pic
        self.updatePic(0)

    def updatePic(self, picIndex = 0):
        """Changes to the next pic to judge for the user."""
        try:
            currentPic = self.listOfPics[picIndex]
            self.picLabel.setPixmap(QPixmap(currentPic).scaledToHeight(self.picLabel.size().height()))
            self.statusbar.showMessage(f"{currentPic}")
        except IndexError: # no more pics.
            self.finish()

    def finish(self):
        """
        Get's called after all images were judged
        """
        for button in (self.posPushButton, self.negPushButton):
            button.setEnabled(False)
        for pics in ((self.neg2do, self.negPics), (self.pos2do, self.posPics)):
            if pics[0] == "txt":
                self.CreateTxtFileFromList(pics[1])

    def CreateTxtFileFromList(self, listOfJudgedPics: list):
        """Writes the paths of all judged pics (neg/pos) into a .txt file"""
        if listOfJudgedPics == self.negPics:
            fileName = "false.txt"
        else:
            fileName = "true.txt"
        with open(fileName, "w") as file:
            file.write("\n".join(listOfJudgedPics))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PolliceVerso()
    window.showMaximized()
    app.exec()