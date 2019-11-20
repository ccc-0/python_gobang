from PySide2.QtWidgets import QWidget,QPushButton,QApplication,QLabel
from PySide2.QtGui import QPalette,QImage,QBrush,QPixmap
from PySide2.QtCore import Signal
from Base import Basewindow
import os,PySide2,sys

dirname = os.path.dirname(PySide2.__file__)
plugin_path = os.path.join(dirname, 'plugins', 'platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path

# 自定义棋子类型
class Chessman(QLabel):

    def __init__(self,color=False,parent=None):
        super().__init__(parent)

        # 0 黑 1 白
        if color:
            self.setPixmap(QPixmap('source/黑子.png'))
        else:
            self.setPixmap(QPixmap('source/白子.png'))
        self.x_index = 0
        self.y_index = 0
        self.color = color

    def getindex(self,x,y):
        # 计算棋子位置、数组索引序号
        self.x_index = (x-50+15)//30
        self.y_index = (y-50+15)//30
        x = 50 + self.x_index*30
        y = 50 + self.y_index*30
        return x,y

class win(QLabel):
    def __init__(self,color=False,parent=None):
        super().__init__(parent)
        if color:
            self.setPixmap(QPixmap('source/黑棋胜利.png'))
        else:
            self.setPixmap(QPixmap('source/白棋胜利.png'))


class Doublewindow(Basewindow):
    # 自定义信号
    back = Signal(str)   #pyqtsignal()
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setWindowTitle('双人对战')
        # self.biaoshi= QLabel.setPixmap(PySide2.QtGui.QPixmap('source/标识.png'))

        self.record=[]
        self.wintu = []
        #标记
        self.xiaqiflag = False
        self.whowinflag =False
        self.huiqiflag =False
        # False 黑色,True 白色
        self.chessmanColor = False
        # 空白棋盘
        self.chessboard = [[ None for x in range(19)] for x in range(19)]

        # 绑定返回事件
        self.backBtn.clicked.connect(self.backSlot)
        #开始
        self.startBtn.clicked.connect(self.startgame)
        #悔棋
        self.regretBtn.clicked.connect(self.regret)
        #认输
        self.loseBtn.clicked.connect(self.losegame)

    # 返回主界面槽函数
    def backSlot(self):
        self.back.emit("传参测试")

    def startgame(self):
        # 重新开始 1 清空棋盘 2 清空记录表 3 重置开始标志 4 隐藏胜利labal
        for x in self.record:                  # 清空黑棋白棋图片
            x.close()
        self.record = []   # 2
        self.chessmanColor = False
        self.chessboard = [[None for x in range(19)] for x in range(19)] # 1
        self.xiaqiflag =True    # 3
        self.huiqiflag =False
        # self.whowin=win(self.chessmanColor,parent=self)
        if self.whowinflag:
            for x in self.wintu:
                x.close()
            # del self.wintu # 4
            # self.whowin.close()
                self.wintu=[]

    def regret(self):
        if self.huiqiflag:
            return
        self.tmp = self.record.pop()
        self.tmp.deleteLater()
        self.chessboard[self.tmp.y_index][self.tmp.x_index]=None
        self.chessmanColor = not self.chessmanColor

    def losegame(self):
        if self.xiaqiflag ==False:
            return
        self.xiaqiflag=False
        self.whowin=win(self.chessmanColor,parent=self)
        self.whowin.move(60,50)
        self.whowin.show()
        self.wintu.append(self.whowin)
        self.whowinflag=True

    # 重写鼠标按下事件
    def mousePressEvent(self, event:PySide2.QtGui.QMouseEvent):
        # event.pos()
        x = event.x()
        y = event.y()
        if self.xiaqiflag ==True:
            # 判断 - 如果超出返回，直接返回，不做任何操作
            if x < 50-15 or x > 590+15:
                return
            if y < 50-15 or y > 590+15:
                return
            if self.chessboard[(y-50+15)//30][(x-50+15)//30]:
                return
            # chessmanColor 记录了当前棋子颜色，当前是白色，那么下一个棋子因为黑色
            self.chessmanColor = not self.chessmanColor
            # 实例化一个棋子
            self.chessman = Chessman(self.chessmanColor,parent=self)
            # 计算棋子棋盘坐标和数组索引，返回棋盘坐标
            x,y= self.chessman.getindex(x,y)
            # 移动并显示棋子
            self.chessman.move(x-15, y-15)
            self.chessman.show()
            # self.biaoshi.move(x,y)
            # self.biaoshi.show()
            # 棋子添加到二维数组中
            # self.chessboard[self.chessman.y_index][self.chessman.x_index] = self.chessman
            if self.chessboard[self.chessman.y_index][self.chessman.x_index]==None:
                self.chessboard[self.chessman.y_index][self.chessman.x_index] = self.chessman
                self.record.append(self.chessman)
            else :
                self.chessman.deleteLater()
                self.chessmanColor = not self.chessmanColor

            # self.lastchessman = self.chessman
            # 判断输赢
            self.isWin(self.chessman)
            return True

            # self.hide() #隐藏

    def isWin(self,chessman):
        # 记录判断起始位置
        x = chessman.x_index
        y = chessman.y_index
        # 当前棋子记录颜色
        color = chessman.color

        def panduan(xcof,ycof):
            # 计数器
            count = 1
            x = chessman.x_index
            y = chessman.y_index
            while (x < 18 and x >= 0)and (y < 18 and y >= 0):
                if self.chessboard[y+ycof][x+xcof] and self.chessboard[y+ycof][x+xcof].color == color:
                    count += 1
                    y += ycof
                    x += xcof
                else:
                    break
                # 如果有5个相连的棋子则为赢
                if count ==5:
                    self.whowin=win(self.chessmanColor,parent=self)
                    self.whowin.move(60,50)
                    self.whowin.show()
                    self.wintu.append(self.whowin)
                    self.xiaqiflag= False
                    self.whowinflag=True
                    self.huiqiflag =True
            x = chessman.x_index
            y = chessman.y_index
            while (x < 18 and x >= 0)and (y < 18 and y >= 0):
                if self.chessboard[y-ycof][x-xcof] and self.chessboard[y-ycof][x-xcof].color == color:
                    count += 1
                    y -= ycof
                    x -= xcof
                else:
                    break
                if count ==5:
                    self.whowin=win(self.chessmanColor,parent=self)
                    self.whowin.move(60,50)
                    self.whowin.show()
                    self.wintu.append(self.whowin)
                    self.xiaqiflag= False
                    self.whowinflag=True
                    self.huiqiflag =True

        if x < 18 or x >= 0 or y < 18 or y >= 0:
            #捺
            panduan(-1,-1)
            panduan(+1,+1)
            #撇
            panduan(-1,+1)
            panduan(+1,-1)
            #竖
            panduan(0,-1)
            panduan(0,+1)
            #横
            panduan(-1,0)
            panduan(+1,0)
        def teshu1(xcof,ycof):
            count = 1
            x = chessman.x_index
            y = chessman.y_index
            while x ==18 and y !=18:
                if self.chessboard[y+ycof][x+xcof] and self.chessboard[y+ycof][x+xcof].color == color:
                    count += 1
                    y += ycof
                    x += xcof
                else:
                    break
                if count ==5:
                    self.whowin=win(self.chessmanColor,parent=self)
                    self.whowin.move(60,50)
                    self.whowin.show()
                    self.wintu.append(self.whowin)
                    self.xiaqiflag= False
                    self.whowinflag=True
                    self.huiqiflag =True
            x = chessman.x_index
            y = chessman.y_index
            while x ==18 and y !=18:
                if self.chessboard[y-ycof][x-xcof] and self.chessboard[y-ycof][x-xcof].color == color:
                    count += 1
                    y -= ycof
                    x -= xcof
                else:
                    break
                if count ==5:
                    self.whowin=win(self.chessmanColor,parent=self)
                    self.whowin.move(60,50)
                    self.whowin.show()
                    self.wintu.append(self.whowin)
                    self.xiaqiflag= False
                    self.whowinflag=True
                    self.huiqiflag =True

        def teshu2(xcof,ycof):
            count = 1
            x = chessman.x_index
            y = chessman.y_index
            while x ==18 and y !=18 :
                if self.chessboard[y+ycof][x+xcof] and self.chessboard[y+ycof][x+xcof].color == color:
                    count += 1
                    y += ycof
                    x += xcof
                while (x < 18 and x >= 0)and (y < 18 and y >= 0):
                    if self.chessboard[y+ycof][x+xcof] and self.chessboard[y+ycof][x+xcof].color == color:
                        count += 1
                        y += ycof
                        x += xcof
                    else:
                        break
                    if count ==5:
                        self.whowin=win(self.chessmanColor,parent=self)
                        self.whowin.move(60,50)
                        self.whowin.show()
                        self.wintu.append(self.whowin)
                        self.xiaqiflag= False
                        self.whowinflag=True
                        self.huiqiflag =True
                else:
                    break
        if x==18  and y!=18:
            teshu1(0,+1)
            teshu1(0,-1)
            teshu2(-1,0)
            teshu2(-1,-1)
            teshu2(-1,+1)

        def teshu3(xcof,ycof):
            count = 1
            x = chessman.x_index
            y = chessman.y_index
            while y ==18 and x !=18:
                if self.chessboard[y+ycof][x+xcof] and self.chessboard[y+ycof][x+xcof].color == color:
                    count += 1
                    y += ycof
                    x += xcof
                else:
                    break
                if count ==5:
                    self.whowin=win(self.chessmanColor,parent=self)
                    self.whowin.move(60,50)
                    self.whowin.show()
                    self.wintu.append(self.whowin)
                    self.xiaqiflag= False
                    self.whowinflag=True
                    self.huiqiflag =True

            x = chessman.x_index
            y = chessman.y_index
            while y ==18 and x !=18:
                if self.chessboard[y-ycof][x-xcof] and self.chessboard[y-ycof][x-xcof].color == color:
                    count += 1
                    y -= ycof
                    x -= xcof
                else:
                    break
                if count ==5:
                    self.whowin=win(self.chessmanColor,parent=self)
                    self.whowin.move(60,50)
                    self.whowin.show()
                    self.wintu.append(self.whowin)
                    self.xiaqiflag= False
                    self.whowinflag=True
                    self.huiqiflag =True
        def teshu4(xcof,ycof):
            count = 1
            x = chessman.x_index
            y = chessman.y_index
            while y ==18 and x !=18:
                if self.chessboard[y+ycof][x+xcof] and self.chessboard[y+ycof][x+xcof].color == color:
                    count += 1
                    y += ycof
                    x += xcof
                    while (x < 18 and x >= 0)and (y < 18 and y >= 0):
                        if self.chessboard[y+ycof][x+xcof] and self.chessboard[y+ycof][x+xcof].color == color:
                            count += 1
                            y += ycof
                            x += xcof
                        else:
                            break
                        if count ==5:
                            self.whowin=win(self.chessmanColor,parent=self)
                            self.whowin.move(60,50)
                            self.whowin.show()
                            self.wintu.append(self.whowin)
                            self.xiaqiflag= False
                            self.whowinflag=True
                            self.huiqiflag =True
                else:
                    break
        if y==18and x !=18:
            teshu3(+1,0)
            teshu3(-1,0)
            teshu4(0,-1)
            teshu4(-1,-1)
            teshu4(+1,-1)

        def teshu5(xcof,ycof):
            count = 1
            x = chessman.x_index
            y = chessman.y_index
            while y ==18 and x ==18:
                if self.chessboard[y+ycof][x+xcof] and self.chessboard[y+ycof][x+xcof].color == color:
                    count += 1
                    y += ycof
                    x += xcof
                    while (x < 18 and x >= 0)and (y < 18 and y >= 0):
                        if self.chessboard[y+ycof][x+xcof] and self.chessboard[y+ycof][x+xcof].color == color:
                            count += 1
                            y += ycof
                            x += xcof
                        else:
                            break
                        if count ==5:
                            self.whowin=win(self.chessmanColor,parent=self)
                            self.whowin.move(60,50)
                            self.whowin.show()
                            self.wintu.append(self.whowin)
                            self.xiaqiflag= False
                            self.whowinflag=True
                            self.huiqiflag =True
                    while (x < 18 and x >= 0)and y==18:
                        if self.chessboard[y+ycof][x+xcof] and self.chessboard[y+ycof][x+xcof].color == color:
                            count += 1
                            y += ycof
                            x += xcof
                        else:
                            break
                        if count ==5:
                            self.whowin=win(self.chessmanColor,parent=self)
                            self.whowin.move(60,50)
                            self.whowin.show()
                            self.wintu.append(self.whowin)
                            self.xiaqiflag= False
                            self.whowinflag=True
                            self.huiqiflag =True
                    while x==18 and (y < 18 and y >= 0):
                        if self.chessboard[y+ycof][x+xcof] and self.chessboard[y+ycof][x+xcof].color == color:
                            count += 1
                            y += ycof
                            x += xcof
                        else:
                            break
                        if count ==5:
                            self.whowin=win(self.chessmanColor,parent=self)
                            self.whowin.move(60,50)
                            self.whowin.show()
                            self.wintu.append(self.whowin)
                            self.xiaqiflag= False
                            self.whowinflag=True
                            self.huiqiflag =True
                else:
                    break
        if x ==18 and y ==18:
            teshu5(-1,-1)
            teshu5(-1,0)
            teshu5(0,-1)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Doublewindow()
    w.show()
    sys.exit(app.exec_())


