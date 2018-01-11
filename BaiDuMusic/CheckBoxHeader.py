from PyQt5.QtCore import Qt, QRect
from  PyQt5.QtWidgets import QTableWidget, QApplication, QHeaderView, QStyleOptionButton, QStyle
from PyQt5.QtCore import pyqtSlot,pyqtSignal

import sys

# refer: http://blog.csdn.net/liukang325/article/details/49682901

class CheckBoxHeader(QHeaderView):

    # isChecked = False

    def __init__(self, checkColumnIndex=0, orientation=Qt.Horizontal, parent=None):
        QHeaderView.__init__(self, orientation, parent)
        self.m_checkColIdx = checkColumnIndex
        self.isChecked = False

    @pyqtSlot(bool)
    def checkStatusChanged(self, checked):
        pass

    def paintSection(self, painter, rect, logicalIndex):
        painter.save()
        QHeaderView.paintSection(self, painter, rect, logicalIndex)
        painter.restore()
        if logicalIndex == self.m_checkColIdx:
            option = QStyleOptionButton()
            option.rect = QRect(5, 5, 21, 15)
            if self.isChecked:
                option.state = QStyle.State_On
            else:
                option.state = QStyle.State_Off
            self.style().drawControl(QStyle.CE_CheckBox, option, painter)

    def mousePressEvent(self, event):
        if self.logicalIndexAt(event.pos().x()) == self.m_checkColIdx:
            self.isChecked = not self.isChecked
            self.updateSection(self.m_checkColIdx)
            self.checkStatusChanged(self.isChecked)

        QHeaderView.mousePressEvent(self, event)
#
# class MyTable(QTableWidget):
#     def __init__(self):
#         QTableWidget.__init__(self, 3, 3)
#
#         myHeader = CheckBoxHeader(Qt.Horizontal, self)
#         self.setHorizontalHeader(myHeader)
#
#         self.setHorizontalHeaderLabels(['', 'A', 'B'])
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     myTable = MyTable()
#     myTable.show()
#     sys.exit(app.exec_())