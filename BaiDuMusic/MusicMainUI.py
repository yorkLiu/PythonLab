# -*- coding: UTF-8 -*-

import sys
from PyQt5.QtWidgets import (QApplication,QDesktopWidget, QMainWindow, QAction, QMessageBox)
from PyQt5.QtGui import QIcon
from MusicWidget import MusicWidget
import MessageResource as MsgRes

class MusicMainUI(QMainWindow):

    def __init__(self, parent=None):
        super(MusicMainUI, self).__init__(parent)

        self.initUI()

    def initUI(self):
        self.setWindowIcon(QIcon('res/icon.png'))
        self.statusBar().showMessage('')

        # exit icon
        exitAct = QAction(QIcon('res/exit.png'), '退出程序', self)
        exitAct.setShortcut('Ctrl+q')
        exitAct.setStatusTip('退出程序')
        exitAct.triggered.connect(self.closeProgram)

        # setting icon
        settingAct = QAction(QIcon('res/setting.png'), '设置', self)
        settingAct.setShortcut('Ctrl+Alt+S')
        settingAct.setStatusTip('设置')
        settingAct.triggered.connect(self.settingHandler)


        # menubar = self.menuBar()
        # menubar.setNativeMenuBar(False)
        # fileMenu = menubar.addMenu('&File')
        # fileMenu.addAction(exitAct)

        toolbar = self.addToolBar('')
        toolbar.addAction(exitAct)
        toolbar.addAction(settingAct)




        self.setCentralWidget(MusicWidget(self))


        self.setWindowTitle(MsgRes.program_name)
        self.setGeometry(0, 0, 800, 600)
        self.center()


    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width())/2, (screen.height()-size.height())/2)

    def closeProgram(self):
        m = QMessageBox()
        m.setWindowTitle(MsgRes.program_name)
        m.setText(MsgRes.program_confirm_exit_msg_text)
        # m.setInformativeText('Are you sure you want exit this program?')
        m.addButton(QMessageBox.Yes)
        m.addButton(QMessageBox.No)
        m.setDefaultButton(QMessageBox.No)
        m.setIcon(QMessageBox.Question)

        receipt = m.exec_()

        # receipt = m.question(self, 'Message', 'Are you sure you want exit this program?', QMessageBox.Yes, QMessageBox.No)
        if receipt == QMessageBox.Yes:
            self.close()


    def settingHandler(self):
        pass

if __name__ == '__main__':

     app = QApplication(sys.argv)

     w = MusicMainUI()
     w.show()
     sys.exit(app.exec_())