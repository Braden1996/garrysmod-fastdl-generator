# Name: BZ2 Folder Compression
# Author: Braden1996
# Description: This goes through and compresses every file in the source directory
# and saves the result to the output directory. It was designed for use with FastDL
# for the big-booty-bitches.com community

from PyQt4.QtCore import *
from PyQt4.QtGui import *

class CustomTitlebar(QWidget):

    def __init__(self, parent):
        super(CustomTitlebar, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.closeBtn = QPushButton("X", self)
        self.closeBtn.setObjectName("close")
        self.closeBtn.setCursor(Qt.PointingHandCursor)
        self.closeBtn.clicked.connect(self.onClose)

        self.label = QLabel(self)

    def onClose(self):
        try:
            self.parent().onClose()
        except AttributeError:
            pass

    def mousePressEvent(self, event):
        self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if not hasattr(self, "offset"): return

        scr = QApplication.desktop().screenGeometry()
        scrH = scr.height()
        scrW = scr.width()

        size = self.parent().size()
        w = size.width()
        h = size.height()

        x = event.globalX() - self.offset.x()
        y = event.globalY() - self.offset.y()
        self.parent().move(x, y)

    def paintEvent(self, event):
        QWidget.paintEvent(self, event)
        painter = QStylePainter(self)
        opt = QStyleOptionFrame()
        opt.initFrom(self)
        painter.drawPrimitive(QStyle.PE_Widget, opt)

    def doLayout(self):
        w = self.parent().size().width()
        h = 50
        m = 4

        self.resize(w, h)

        btnH = h - 2*m
        btnW = btnH*2
        self.closeBtn.resize(btnH*2, btnH)
        self.closeBtn.move(w - btnW - m, m)
        return w, h
