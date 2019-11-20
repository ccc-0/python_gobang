import os,PySide2,sys
from PySide2.QtWidgets import QApplication,QPushButton,QWidget
from PySide2.QtCore import *
from PySide2.QtGui import *
from DoublePlayer import Doublewindow
from SinglePlayer import Singlewindow
from NetPlayer import *
from MyButton import Mybutton

dirname = os.path.dirname(PySide2.__file__)
plugin_path = os.path.join(dirname, 'plugins', 'platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path

class Mainwindow(QWidget):
    def __init__(self,parent=None):
        super().__init__(parent)
        # 设置标题、图标
        self.setWindowTitle("五子棋")
        self.setWindowIcon(QIcon('source/icon.ico'))

        # 绘制背景
        p = QPalette(self.palette())  # 新建一个调色板
        b = QBrush(QImage('source/五子棋界面.png')) # 新建一个画刷
        p.setBrush(QPalette.Background,b) # 为调色板设置画刷
        self.setPalette(p)    # 设置当前窗口调色板
        self.setFixedSize(760,650)

        self.singlebtn = Mybutton('source/人机对战_normal.png',
                                  'source/人机对战_hover.png',
                                  'source/人机对战_press.png',parent=self)
        self.singlebtn.move(300,300)
        self.doublebtn = Mybutton('source/双人对战_normal.png',
                                  'source/双人对战_hover.png',
                                  'source/双人对战_press.png',
                                  parent=self)
        self.doublebtn.move(300,400)
        self.netbtn = Mybutton('source/联机对战_normal.png',
                                'source/联机对战_hover.png',
                                'source/联机对战_press.png',
                                parent=self)
        self.netbtn.move(300,500)

        # 绑定槽函数，当点击改函数时，执行对应函数
        self.doublebtn.clicked.connect(self.startDoublePlayer)
        self.singlebtn.clicked.connect(self.startSinglePlayer)
        self.netbtn.clicked.connect(self.startNetPlayer)

    def startDoublePlayer(self):
        self.gameWindow = Doublewindow()
        self.gameWindow.back.connect(self.restart)
        # self.gameWindow.loseBtn.clicked.connect(self.restart)
        self.gameWindow.show()
        self.close()
    def startSinglePlayer(self):
        self.gameWindow = Singlewindow()
        self.gameWindow.back.connect(self.restart)
        self.gameWindow.show()
        self.close()

    def startNetPlayer(self):
        self.netconfig =NetConfig()
        self.netconfig.netconfig_back.connect(self.restart2) #返回
        self.netconfig.netconfigBtn_clicked.connect(self.createNetWindow) #进入联机对战窗口
        self.netconfig.show()
        self.close()
    def createNetWindow(self,t,ip,port,name):
        if t =='s':
            self.netObject = NetServer(ip,port,name)
        else:
            self.netObject = NetClient(ip,port,name)
        self.gameWindow =NetPlayerWindow(self.netObject)
        self.gameWindow.back.connect(self.restart)
        self.gameWindow.show()
        self.close()

    def restart(self,a0):
        self.show()
        self.gameWindow.close()
    def restart2(self):
        self.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mianWindow = Mainwindow()
    mianWindow.show()
    sys.exit(app.exec_())
