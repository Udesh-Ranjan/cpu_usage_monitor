#!/usr/bin/env python3.10

import sys
import os
import time

from PySide6.QtWidgets import (QApplication, QMainWindow,
        QWidget, QFrame, QVBoxLayout, QHBoxLayout, QGridLayout,
        QStackedLayout)
from PySide6.QtCore import (Qt)
from PySide6.QtGui import (QColor)

from circular_progress_bar import CircularProgressBar
from core import Core

class MainWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.initUI(app)

    def initUI(self, app):

        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlag(Qt.FramelessWindowHint)

        self.resize(500, 500)

        self.container = QFrame()

        self.layout = QStackedLayout()

        self.cpBars = []
        self.cores = []

        for count in range(os.cpu_count()): 
            circularProgressBar = CircularProgressBar()
            core = Core(_id=count)
            core.call = circularProgressBar.setProgress
            #core.call = lambda core=core, cp = circularProgressBar: cp.setProgress(progress=core.utilisation,
            #        text=f"{core.id} : {core.utilisation}%")
            self.cpBars.append(circularProgressBar)
            self.cores.append(core)

        for index, cpBar in enumerate(self.cpBars):
            self.layout.addWidget(cpBar)

        self.container.setLayout(self.layout)

        self.setCentralWidget(self.container)

        width = app.primaryScreen().size().width()
        height = app.primaryScreen().size().height()

        self.setGeometry((width-self.width())/2,
                (height-self.height())/2,
                self.width(), self.height())

        for core in self.cores:
            core.start()

    def keyReleaseEvent(self, event):
        key = event.key()
        if key == Qt.Key_Left:
            index = self.layout.currentIndex()
            self.layout.setCurrentIndex(len(self.cpBars) -1 if index==0 else index-1)

        if key == Qt.Key_Right:
            index = self.layout.currentIndex()
            self.layout.setCurrentIndex((index+1)%len(self.cpBars))

        if key == Qt.Key_Q:
            self.close()

    def closeEvent(self, event):
        for core in self.cores:
            core.running = False
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    mainWindow = MainWindow(app)
    mainWindow.show()

    sys.exit(app.exec())
