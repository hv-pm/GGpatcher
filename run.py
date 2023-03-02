import os
import platform
import sys
import urllib.request
from io import BytesIO
from os import walk
from zipfile import ZipFile

from PyQt5.QtCore import Qt, QPoint, QCoreApplication, QThread, pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QApplication

from patcher import *
from language import *


class Patcher(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        super().setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.closeBt.clicked.connect(self.closePatcher)
        self.updateBt.clicked.connect(self.gameUpdate)
        self.gameStartBt.released.connect(self.gameStart)
        self.gameStartBt.pressed.connect(self.btHitImg)
        self.optionsBt.clicked.connect(self.gameOptions)
        self.languageBt.clicked.connect(self.languageOptions)

        self.langWin = Ui_LanguageWindow()
        self.langWin.confirmLanguage.connect(self.languageUpdate)

    def mousePressEvent(self, event):
        self.lastPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.lastPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.lastPos = event.globalPos()

    def closePatcher(self):
        QCoreApplication.instance().quit()
        self.close()

    def gameUpdate(self):
        self.auxProgressImg.move(240, self.auxProgressImg.pos().y())
        self.progressBar.setValue(0)
        self.barWorker = UpdateThread()
        self.barWorker.start()
        self.barWorker.updateMax.connect(self.evtBarMax)
        self.barWorker.updateProgress.connect(self.evtUpdateProgress)
        self.barWorker.finished.connect(self.evtEndBarProgress)
        self.languageBt.setEnabled(False)
        self.gameStartBt.setEnabled(False)
        self.updateBt.setEnabled(False)

    def languageUpdate(self):
        self.gameUpdate()

    def evtBarMax(self, val):
        self.progressBar.setMaximum(val)
        self.totalFiles = val

    def evtUpdateProgress(self, val):
        self.progressBar.setValue(val)
        if val == 1:
            self.auxProgress = int(240 + (341 / self.totalFiles))
            self.auxProgressImg.move(self.auxProgress, self.auxProgressImg.pos().y())
        else:
            self.auxProgress = int((341 * val) / self.totalFiles)
            self.auxProgressImg.move(240 + self.auxProgress, self.auxProgressImg.pos().y())

    def evtEndBarProgress(self):
        self.languageBt.setEnabled(True)
        self.gameStartBt.setEnabled(True)
        self.updateBt.setEnabled(True)

    def gameStart(self):
        if platform.system() == 'Windows':
            os.startfile('Game.exe')  # YOUR GAME.EXE PATH
            self.closePatcher()

    def btHitImg(self):
        self.gameStartBt.setStyleSheet(
        "QPushButton{\n"
        "border-radius: 65px;\n"
        "background-image: url(\'./img/playHit.png\');\n"
        "}\n"
        "QPushButton:hover {\n"
        "background-image: url(\'./img/playHit.png\');\n"
        "}\n"
        "QPushButton::pressed {\n"
        "background-image: url(\'./img/playHit.png\');\n"
        "}")

    def gameOptions(self):
        if platform.system() == 'Windows':
            os.startfile('Setup.exe')  # YOUR SETUP.EXE PATH

    def languageOptions(self):
        self.langWin.displayMe()


class UpdateThread(QThread):
    updateProgress = pyqtSignal(int)
    updateMax = pyqtSignal(int)

    def run(self):
        updateFilelist = []
        updateFileListUrl = "http://example.com/downloads/file.format"  # YOUR UPDATE FILELIST URL
        for line in urllib.request.urlopen(updateFileListUrl):
            updateTup = tuple(line.decode('utf-8').replace('\r\n', '').split(','))
            updateFilelist.append(updateTup)

        with open('config.txt', 'r') as f:
            self.curLanguage = f.readlines()
        translatePatchInfoUrl = ""
        translatePatchUrl = ""
        if int(self.curLanguage[0]) == 1:  # (en-us)
            translatePatchInfoUrl = "http://example.com/downloads/file.format"  # YOUR EN-US TRANSLATED DATA FILELIST URL
            translatePatchUrl = urllib.request.urlopen(  
                "http://example.com/downloads/file.format")  # YOUR EN-US TRANSLATED DATA FILE URL
        elif int(self.curLanguage[0]) == 2:  # (pt-br)
            translatePatchInfoUrl = "http://example.com/downloads/file.format"  # YOUR PT-BR TRANSLATED DATA FILELIST URL
            translatePatchUrl = urllib.request.urlopen(  
                "http://example.com/downloads/file.format")  # YOUR PT-BR TRANSLATED DATA FILE URL
        elif int(self.curLanguage[0]) == 3:  # (th)
            translatePatchInfoUrl = "http://example.com/downloads/file.format" # YOUR TH TRANSLATED DATA FILELIST URL
            translatePatchUrl = urllib.request.urlopen(  
                "http://example.com/downloads/file.format")  # YOUR TH TRANSLATED DATA FILE URL
        elif int(self.curLanguage[0]) == 4:  # (zh-cn)
            translatePatchInfoUrl = "http://example.com/downloads/file.format"  # YOUR ZH-CN TRANSLATED DATA FILELIST URL
            translatePatchUrl = urllib.request.urlopen(  
                "http://example.com/downloads/file.format")  # YOUR ZH-CN TRANSLATED DATA FILE URL
        for line in urllib.request.urlopen(translatePatchInfoUrl):
            updateTup = tuple(line.decode('utf-8').replace('\r\n', '').split(','))
            updateFilelist.append(updateTup)

        localDirectory = os.getcwd()
        localFiles = []
        for (dir_path, dir_names, file_names) in walk(localDirectory):
            for x in file_names:
                size = os.stat(os.path.join(dir_path, x)).st_size
                tup = (x, size)
                localFiles.append(tup)

        updateList = []
        for x in updateFilelist:
            if not any(x[0] in y for y in localFiles):
                updateList.append(x[0])
            for y in localFiles:
                if x[0] == y[0]:
                    if int(x[1]) != y[1]:
                        updateList.append(x[0])

        updateFilesUrl = urllib.request.urlopen(  
            "http://example.com/downloads/file.format")  # YOUR UPDATE FILES .ZIP URL
        if len(updateList) == 0:
            bar = 1
            self.updateMax.emit(bar)
            self.updateProgress.emit(bar)
        else:
            self.totalFiles = len(updateList)
            self.updateMax.emit(self.totalFiles)
            bar = 0
            with ZipFile(BytesIO(updateFilesUrl.read()), 'a') as updateZipFile:
                for patchFile in updateZipFile.namelist():
                    for f in updateList:
                        if patchFile.endswith(f):
                            updateZipFile.extract(patchFile, localDirectory)
                            bar += 1
                            self.updateProgress.emit(bar)
            with ZipFile(BytesIO(translatePatchUrl.read()), 'a') as translateZipFile:
                for translateFile in translateZipFile.namelist():
                    translateZipFile.extract(translateFile, localDirectory)
                    if bar != len(updateList):
                        bar += 1
                    self.updateProgress.emit(bar)


if __name__ == '__main__':
    qt = QApplication(sys.argv)
    run = Patcher()
    run.show()
    run.gameUpdate()
    sys.exit(qt.exec_())
