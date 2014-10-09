# Name: BZ2 Folder Compression
# Author: Braden1996
# Description: This goes through and compresses every file in the src directory
# and saves the result to the output directory. It was designed for use with FastDL
# for the big-booty-bitches.com community

from sys import exit as sysExit, argv as sysArgV
from os import getcwd
from os.path import isdir
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from lib.titlebar import CustomTitlebar
from lib.compressfastdl import FastDLFolder
from webbrowser import open as webOpen

class MainWindow(QMainWindow):
    
    def __init__(self):
        super(MainWindow, self).__init__()

        # Internal, just for easy directory
        self.curSrcDir = getcwd()
        self.curOutDir = getcwd()
        
        self.initUI()
        
    def initUI(self):
        self.setGeometry(300, 300, 400, 250)
        self.setMinimumSize(QSize(400, 250))
        self.setMaximumSize(QSize(1000, 225))
        self.setWindowTitle("Garry's Mod FastDL Generator")
        self.setWindowIcon(QIcon("img/icon.png"))
        self.setWindowFlags(Qt.FramelessWindowHint)

        self.titlebar = CustomTitlebar(self)
        self.titlebar.label.setText("Garry's Mod FastDL Generator")

        srcLbl = QLabel("Source Folder:")
        self.srcEdit = QLineEdit()
        srcBtn = QPushButton("...")
        srcBtn.setCursor(Qt.PointingHandCursor)
        def getSrcDir():
            file = str(QFileDialog.getExistingDirectory(None, "Select Source Directory", self.curSrcDir))
            if file is None or file == "":
                self.show()
                return
            self.curSrcDir = file
            self.srcEdit.setText(file)
            self.srcEdit.cursorPosition = len(self.srcEdit.text())
            self.show()
        srcBtn.clicked.connect(getSrcDir)
        srcBtn.setObjectName("dir")

        outLbl = QLabel("Output Folder:")
        self.outEdit = QLineEdit()
        outBtn = QPushButton("...")
        outBtn.setCursor(Qt.PointingHandCursor)
        def getOutDir():
            file = str(QFileDialog.getExistingDirectory(None, "Select Output Directory", self.curOutDir))
            if file is None or file == "":
                self.show()
                return
            self.curOutDir = file
            self.outEdit.setText(file)
            self.outEdit.cursorPosition = len(self.outEdit.text())
            self.show()
        outBtn.clicked.connect(getOutDir)
        outBtn.setObjectName("dir")

        self.resrcCb = QCheckBox("Generate Resource File")
        self.resrcCb.setCursor(Qt.PointingHandCursor)

        self.replaceCb = QCheckBox("Replace Existing Output")
        self.replaceCb.setCursor(Qt.PointingHandCursor)

        executeBtn = QPushButton("Execute")
        executeBtn.setCursor(Qt.PointingHandCursor)
        executeBtn.clicked.connect(self.onExecute)
        executeGmaBtn = QPushButton("Unpack .gma files")
        executeGmaBtn.setCursor(Qt.PointingHandCursor)
        executeGmaBtn.clicked.connect(self.onExecuteGma)
        
        helpBtn = QPushButton("Help")
        helpBtn.setCursor(Qt.PointingHandCursor)
        def OpenHelp():
            webOpen("https://github.com/Braden1996/garrysmod-fastdl-generator")
        helpBtn.clicked.connect(OpenHelp)  

        layout = QGridLayout()
        self.contentPnl = QWidget(self)
        self.contentPnl.setObjectName("ContentPanel")
        self.contentPnl.setLayout(layout)

        layout.addWidget(srcLbl, 0, 0)
        layout.addWidget(self.srcEdit, 0, 1)
        layout.addWidget(srcBtn, 0, 2)
        layout.addWidget(outLbl, 1, 0)
        layout.addWidget(self.outEdit, 1, 1)
        layout.addWidget(outBtn, 1, 2)
        layout.addWidget(self.resrcCb, 2, 0, 1, 1)
        layout.addWidget(self.replaceCb, 2, 1, 1, 2, Qt.AlignRight)
        layout.addWidget(executeBtn, 3, 0, 1, 3)
        layout.addWidget(executeGmaBtn, 4, 0, 1, 3)
        layout.addWidget(helpBtn, 5, 0, 1, 3)

        self.statusbar = self.statusBar()
        self.statusbar.showMessage("Created by Braden1996")

        self.applyStyleSheet("default")
        self.show()

    def resizeEvent(self, resizeEvent):
        w, h = self.titlebar.doLayout()
        self.contentPnl.move(4, h + 4)
        self.contentPnl.resize(w - 8, self.size().height() - h - 23)

    def applyStyleSheet(self, styleName):
        self.styleSheetName = styleName
        with open("lib/styles/" + styleName + ".css", "r") as style:
            styleSheet = style.read()
            self.setStyleSheet(styleSheet)
            self.titlebar.setStyleSheet(styleSheet)

    def onClose(self):
        self.close()
        sysExit()

    def onExecute(self):
        self.statusbar.showMessage("Working! Please wait.")
        srcDir = self.srcEdit.text()
        if srcDir == "" or not isdir(srcDir):
            self.statusbar.showMessage("You're source directory is invalid!")
            return False

        outDir = self.outEdit.text()
        if outDir == "":
            self.statusbar.showMessage("You're output directory is invalid!")
            return False

        tmpCompress = FastDLFolder(self.statusbar, 1)
        tmpCompress.setSourceDir(srcDir)
        tmpCompress.setOutputDir(outDir)
        if self.replaceCb.checkState() > 0:
            tmpCompress.replaceOld = True
        else:
            tmpCompress.replaceOld = False
        if self.resrcCb.checkState() > 0:
            tmpCompress.generateResource = True
        else:
            tmpCompress.generateResource = False
        tmpCompress.runCompression()

    def onExecuteGma(self):
        self.statusbar.showMessage("Working! Please wait.")
        srcDir = self.srcEdit.text()
        if srcDir == "" or not isdir(srcDir):
            self.statusbar.showMessage("You're source directory is invalid!")
            return False

        outDir = self.outEdit.text()
        if outDir == "":
            self.statusbar.showMessage("You're output directory is invalid!")
            return False

        tmpCompress = FastDLFolder(self.statusbar, 2)
        tmpCompress.setSourceDir(srcDir)
        tmpCompress.setOutputDir(outDir)
        if self.replaceCb.checkState() > 0:
            tmpCompress.replaceOld = True
        else:
            tmpCompress.replaceOld = False
        if self.resrcCb.checkState() > 0:
            tmpCompress.generateResource = True
        else:
            tmpCompress.generateResource = False
        tmpCompress.unpackGma()

        
def main():
    app = QApplication(sysArgV)
    ex = MainWindow()
    sysExit(app.exec_())

if __name__ == "__main__":
    main()    

