from PySide2.QtWidgets import QLabel
from PySide2.QtGui import QPixmap
from PySide2.QtCore import Signal
import os,PySide2,sys

dirname = os.path.dirname(PySide2.__file__)
plugin_path = os.path.join(dirname, 'plugins', 'platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path

class Mybutton(QLabel):
    clicked = Signal()

    def __init__(self,*args,parent=None):
        super().__init__(parent)

        # 1 正常 2 进入 3 按下
        self.pic_1 = QPixmap(args[0])
        self.pic_2 = QPixmap(args[1])
        self.pic_3 = QPixmap(args[2])

        # 默认显示正常图片 及pic_1
        self.setFixedSize(self.pic_1.size())
        self.setPixmap(self.pic_1)

        self.enterFlag = False

    def enterEvent(self, event:PySide2.QtCore.QEvent):
        # 重写鼠标进入事件
        # 鼠标移入时，显示第二张图片
        self.setPixmap(self.pic_2)
        self.enterFlag = True


    def leaveEvent(self, event:PySide2.QtCore.QEvent):
        # 重写鼠标离开事件
        # 鼠标移除时，显示默认图片
        self.setPixmap(self.pic_1)
        self.enterFlag = False


    def mousePressEvent(self, ev:PySide2.QtGui.QMouseEvent):
        self.setPixmap(self.pic_3)

    def mouseReleaseEvent(self, ev:PySide2.QtGui.QMouseEvent):
        if self.enterFlag:
            self.setPixmap(self.pic_2)
            # 如果鼠标弹起在label上时发射点击信号
            self.clicked.emit()
        else:
            self.setPixmap(self.pic_1)

