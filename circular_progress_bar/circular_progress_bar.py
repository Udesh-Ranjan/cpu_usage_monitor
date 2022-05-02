import sys
import random

from PySide6.QtWidgets import (QApplication, QMainWindow,
        QWidget)
from PySide6.QtCore import (Qt, QRect)
from PySide6.QtGui import (QColor, QPainter, QBrush, QPen)

class CircularProgressBar(QWidget):

    colors = ["red", "yellow", "pink", "purple"]

    def __init__(self, text=None):
        print("Called")
        super().__init__()
        #self.setMinimumSize(300, 300)
        self.initUI()
        self.text = text 
        self.progress = 0
        #color = self.colors[random.randint(0, len(self.colors)-1)] 
        #print(f"{color=}")
        #bc = "{"+f"background-color:{color};"+"}"
        #self.setStyleSheet("background-color: yellow")
        #self.setStyleSheet(bc)
        #print(bc)
        #self.setStyleSheet(f"background-color : red;")

    def initUI(self):
        self.penWidth = 5
        self.margin = self.penWidth

    def paintEvent(self, event):
        painter = QPainter()

        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)

        rect = QRect(self.margin, self.margin, self.width()-self.margin*2,
                self.height()-self.margin*2)

        print(self.text, rect)

        brush = QBrush(QColor("#9a00a8"))
        pen = QPen()
        pen.setWidth(self.penWidth)
        pen.setBrush(brush)
        pen.setCapStyle(Qt.RoundCap)
        pen.setJoinStyle(Qt.RoundJoin)
        pen.setStyle(Qt.SolidLine)
        painter.setPen(pen)
        painter.drawArc(rect, 90*16, -(360*self.progress/100)*16)

        if self.text:
            font = painter.font()
            font.setPixelSize(20)
            painter.setFont(font)
            pen.setBrush(QBrush(QColor("#95ff00")))
            painter.setPen(pen)
            painter.drawText(rect, Qt.AlignCenter, f"{self.text}")
        #pen.setBrush(QColor(255, 0, 255))
        #painter.setPen(pen)
        #painter.drawRect(rect)
        painter.end()
        pass

    def setProgress(self, progress=0, text=None):
        self.progress = progress
        print(f"{progress=} {text=}")
        if text:
            self.text = text 
        self.update()
