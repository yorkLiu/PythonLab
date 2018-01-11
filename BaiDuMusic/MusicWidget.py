# -*- coding: UTF-8 -*-
import sys
import functools
from threading import Thread
import time
import MessageResource as MsgRes
from PyQt5.QtWidgets import (QApplication,QWidget,QDesktopWidget,QLabel, QLineEdit, QGridLayout, QHBoxLayout,
                             QTableWidget, QHeaderView, QTableWidgetItem, QAbstractItemView, QPushButton)
from PyQt5.QtCore import Qt, QObject, pyqtSignal, QEvent, QSize, QTimer
from PyQt5.QtGui import QCursor, QIcon
from MusicService import MusicService
from MusicInfo import MusicInfo
from CheckBoxHeader import CheckBoxHeader
from Utils import CustomTimer


def clickable(widget):
    class Filter(QObject):

        clicked = pyqtSignal()

        def eventFilter(self, obj, event):

            if obj == widget:
                if event.type() == QEvent.MouseButtonRelease:
                    if obj.rect().contains(event.pos()):
                        self.clicked.emit()
                        # The developer can opt for .emit(obj) to get the object within the slot.
                        return True

            return False

    filter = Filter(widget)
    widget.installEventFilter(filter)
    return filter.clicked

class MusicWidget(QWidget):
    def __init__(self, parent=None):
        super(MusicWidget, self).__init__(parent)

        self.selectedMusicsSet = set()
        self.musicService = MusicService()
        self.statusBar = parent.statusBar() if parent else None

        self.columnValues = MusicInfo.getItemIndex()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Music")
        self.setGeometry(0, 0, 800, 600)
        # alignment to center
        self.center()

        search_label=QLabel('%s:' % MsgRes.search_label_text)
        self.searchEditor = QLineEdit()
        self.searchEditor.setPlaceholderText(MsgRes.search_editer_placehoder)
        self.searchEditor.setFocus()
        self.searchEditor.keyPressEvent = self.onSearchHandler

        tagsLayout = self.addHotTags(MsgRes.show_hot_categories)


        self.downloadButton = QPushButton(MsgRes.download_button_text)
        self.downloadButton.setDisabled(True)
        self.downloadButton.setIcon(QIcon('res/download.png'))
        self.downloadButton.setIconSize(QSize(16,16))
        self.downloadButton.setMaximumWidth(150)
        self.downloadButton.clicked.connect(self.downloadMusic)

        self.addTable()


        m_layout = QGridLayout()
        m_layout.addWidget(search_label, 0, 0)
        m_layout.addWidget(self.searchEditor, 0, 1)

        m_layout.addItem(tagsLayout, 1, 1)

        m_layout.addWidget(self.downloadButton, 2, 0, 1, 2, Qt.AlignRight)

        m_layout.addWidget(self.songListTable, 3, 0, 1, 2)

        # init the table's data
        self.searchMusicByTagInNewThread()

        self.setLayout(m_layout)


    def addHotTags(self,tags):
        """
        :param tags: [{id, name)}]
        :return:
        """
        tagsLayout = QHBoxLayout()
        for tag in tags:
            tag_id = tag['id']
            tag_name = tag['name']
            label = QLabel(tag_name)
            label.setStyleSheet("QLabel{color:blue}")
            label.setCursor(QCursor(Qt.PointingHandCursor))
            clickable(label).connect(functools.partial(self.searchByTag, str(tag['id'])))
            tagsLayout.addWidget(label)

        return tagsLayout

    def addTable(self):
        self.songListTable = QTableWidget()
        # hide the vertical header
        self.songListTable.verticalHeader().setVisible(False)
        self.songListTable.setColumnCount(5)
        self.songListTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.songListTable.setShowGrid(False)


        header = CheckBoxHeader(0,Qt.Horizontal, self.songListTable)
        self.songListTable.setHorizontalHeader(header)
        header.checkStatusChanged = self.checkAllHandler

        for i in (2,4):
            self.songListTable.horizontalHeader().setSectionResizeMode(i,QHeaderView.Stretch)


        self.songListTable.setHorizontalHeaderLabels(MsgRes.result_list_cols)

        self.songListTable.setColumnHidden(1, True)
        self.songListTable.setColumnWidth(0, 30)

        self.songListTable.itemChanged.connect(self.musicItemChanged)

    def addRow(self, musicInfo):
        rowCount = self.songListTable.rowCount()
        self.songListTable.insertRow(rowCount)
        self.songListTable.setRowHeight(rowCount, MsgRes.row_height)

        for idx,v in enumerate(self.columnValues):
            value = musicInfo.__getattribute__(v) if idx != 0 else musicInfo.__getattribute__('song_id')
            item = QTableWidgetItem()

            if idx == 0:
                item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                item.setCheckState(Qt.Unchecked)

            item.setTextAlignment(Qt.AlignLeft)
            # item.setText(unicode(value).decode('utf-8'))
            item.setText(value)
            # item.setData(idx, value)
            self.songListTable.setItem(rowCount, idx, item)

    def checkAllHandler(self, checked):
        """
        Selected all check box
        :param checked:
        :return:
        """
        for i in range(self.songListTable.rowCount()):
            item = self.songListTable.item(i, 0)
            if item:
                item.setCheckState(Qt.Checked if checked else Qt.Unchecked)

    def clearTableRows(self):
        self.selectedMusicsSet.clear()
        self.songListTable.setRowCount(0)

    def searchMusicByTagInNewThread(self, tagId=MsgRes.default_search_type_id):
        Thread(target=self.searchMusicByTag, args=(tagId,)).start()

    def searchMusicByTag(self, tagId=MsgRes.default_search_type_id):
        self.clearTableRows()
        for c in self.musicService.findMusicByCategory(tagId):
            self.addRow(c)

    def searchMusic(self, searchText):
        results = self.musicService.searchMusic(searchText)
        # clear previous data
        self.clearTableRows()

        if results and len(results) > 0:
            for m in results:
                self.addRow(m)


    def onSearchHandler(self, event):
        QLineEdit.keyPressEvent(self.searchEditor, event)

        if event.key() in (Qt.Key_Enter, Qt.Key_Return):
            self.searchMusic(self.searchEditor.text())

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width())/2, (screen.height()-size.height())/2)

    def enableDownloadButton(self):
        """
        control is enable download button
        :return:
        """
        self.downloadButton.setDisabled(len(self.selectedMusicsSet) == 0)


    def musicItemChanged(self, item):
        row = item.row()
        state = item.checkState()
        songId = item.text()

        if state == 2:
            # checked
            if songId:
                self.selectedMusicsSet.add(str(songId))

        elif state == 0:
            # uncheck
            if songId and len(self.selectedMusicsSet) > 0:
                self.selectedMusicsSet.remove(str(songId))
        else:
            print("Something is not working fine here")

        # control is enable download button
        self.enableDownloadButton()

    def updateStatusBar2(self):
        total = len(self.selectedMusicsSet)

        reminder = self.musicService.getReminderDownload()

        while reminder > 0:
            print '正在下载 [%s/%s]' % (total, (total - reminder))
            if self.statusBar:
                self.statusBar.showMessage('正在下载 [%s/%s]' % (total, (total - reminder)))
                time.sleep(1)

            reminder = self.musicService.getReminderDownload()

        # for i in range(total):
        #     t = CustomTimer(1, self.musicService.getReminderDownload)
        #     t.start()
        #     reminder = t.join()
        #
        #     print '正在下载 [%s/%s]' % (total, (total-reminder))
        #     if self.statusBar:
        #         self.statusBar.showMessage('正在下载 [%s/%s]' % (total, (total-reminder)))


    def downloadMusic(self):
        self.statusBar.showMessage('Downloading....')
        if len(self.selectedMusicsSet) > 0:
            # timer = QTimer()
            # timer.setInterval(1000)
            # timer.timeout.connect(self.updateStatusBar2)
            # timer.start()
            # timer.disconnect()
            # self.musicService.downloadMusic(self.selectedMusicsSet)


            # 非阻塞 download
            t = Thread(target=self.musicService.downloadMusicWithMultipleProcess, args=(self.selectedMusicsSet,))
            t.start()

            time.sleep(1)
            tt = Thread(target=self.updateStatusBar2)
            tt.start()
            # 阻塞 download
            # self.musicService.downloadMusicWithMultipleProcess(self.selectedMusicsSet)
        else:
            pass

    def searchByTag(self, tagId):
        self.searchMusicByTag(tagId)

if __name__ == '__main__':

     app = QApplication(sys.argv)

     w = MusicWidget()
     w.show()
     w.searchMusicByTag()

     sys.exit(app.exec_())