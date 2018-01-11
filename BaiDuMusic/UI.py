# -*- coding: UTF-8 -*-


import sys
from PyQt5.QtWidgets import (QApplication,QWidget,QDesktopWidget,QLabel, QLineEdit, QGridLayout,
                             QTableView, QMainWindow, QToolBar, QMenuBar, QAction,qApp)
from PyQt5.QtGui import QIcon

class MusicUI(QMainWindow):
    def __init__(self, parent=None):
        super(MusicUI, self).__init__(parent)
        self.initUI()

    def initUI(self):


        exitAct = QAction(QIcon('exit.png'), '&Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(qApp.quit)


        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        # menubar.setNativeMenuBar(False)
        fileMenu.addAction(exitAct)

        self.statusBar().showMessage('Ready')

        self.setWindowTitle("Music")
        self.setGeometry(0, 0, 800, 600)
        self.center()





    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width())/2, (screen.height()-size.height())/2)


if __name__ == '__main__':

     app = QApplication(sys.argv)
     w = MusicUI()
     w.show()
     sys.exit(app.exec_())



