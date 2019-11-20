from PySide2.QtWidgets import  QWidget,QPushButton,QLineEdit,QGridLayout,QLabel,QMessageBox
from PySide2.QtCore import Signal,QObject
from PySide2.QtMultimedia import QSound
import socket
import threading
from DoublePlayer import *
import json
from MyButton import Mybutton
# import PySide2


#网络配置窗口
class NetConfig(QWidget):
    netconfig_back = Signal()
    netconfigBtn_clicked = Signal([str,str,str,str])

    def __init__(self,parent=None):
        super().__init__(parent)
        self.name_label =QLabel("玩家名称",self)
        self.name_edit  = QLineEdit("玩家一",self)
        self.ip_label   = QLabel("IP",self)
        self.ip_edit    = QLineEdit("127.0.0.1",self)
        self.port_label = QLabel("PORT",self)
        self.port_edit  = QLineEdit("10086",self)
        self.server_btn =QPushButton("服务器",self)
        self.client_btn =QPushButton("客户端",self)
        g = QGridLayout()
        g.addWidget(self.name_label,0,1)  #( , 行,列)
        g.addWidget(self.name_edit,0,2)
        g.addWidget(self.ip_label,1,1)
        g.addWidget(self.ip_edit,1,2)
        g.addWidget(self.port_label,2,1)
        g.addWidget(self.port_edit,2,2)
        g.addWidget(self.server_btn,3,1)
        g.addWidget(self.client_btn,3,2)
        self.setLayout(g)

        self.server_btn.clicked.connect(self.serverSlot)
        self.client_btn.clicked.connect(self.clientSlot)

    def serverSlot(self):
        self.netconfigBtn_clicked.emit("s",self.ip_edit.text(),self.port_edit.text(),\
                                       self.name_edit.text())
        # self.close()
        self.hide()
    def clientSlot(self):
        self.netconfigBtn_clicked.emit("c",self.ip_edit.text(),self.port_edit.text(),\
                                       self.name_edit.text())
        self.hide()

    def closeEvent(self, event):
        self.netconfig_back.emit()
        self.close()


#游戏界面
class NetPlayerWindow(Doublewindow):
    def __init__(self,netObject,parent =None):
        super().__init__(parent)
        self.setWindowTitle("联机对战")
        self.netObject = netObject
        self.netObject.netConnect()
        self.netObject.msg_signal.connect(self.parseMsg)
        #是否是自己回合的标记
        self.isOwnflag = False
        #催促按钮
        self.cuicuBtn = Mybutton('source/催促按钮_normal.png',
                                 'source/催促按钮_hover.png',
                                 'source/催促按钮_press.png',parent=self)
        self.cuicuBtn.move(630,350)
        self.cuicuBtn.clicked.connect(self.kuaidian)

    def kuaidian(self): #加一个线程播放那个音乐
        th = threading.Thread(target=self.cuicu)
        th.setDaemon(True)
        th.start()
        data = {'msg':'kuaidian'}
        self.netObject.send(json.dumps(data))
        print('ddd')
    def cuicu(self):
        sound = PySide2.QtMultimedia.QSound('source/cuicu.wav')

    def parseMsg(self,data):
        print(data)
        data =json.loads(data)  #把json格式转换为字典格式
        if data['msg'] == 'position':
            x_index = data['x']
            y_index = data['y']
            #棋盘落子
            self.autoChess(x_index,y_index)
        elif data['msg'] == 'start':
            res = QMessageBox.information(self,"是否开始","是否同意开始",QMessageBox.Yes|QMessageBox.No)
            print(res)
            if res == QMessageBox.Yes:
                super().startgame()
                data = {
                    'msg':'res',
                    'res_type':'start',
                    'res_data':'yes'
                }
                self.isOwnflag =False
                self.netObject.send(json.dumps(data))
            else:
                data = {
                    'msg': 'res',
                    'res_type': 'start',
                    'res_data': 'no'
                }
                self.netObject.send(json.dumps(data))
        elif data['msg'] == 'res':
            if data['res_type'] == 'start':
                if data['res_data'] == 'yes':
                    super().startgame()
                    self.isOwnflag = True
                else:
                    QMessageBox.information(self,"提示","对方拒绝",QMessageBox.Close)

        elif data['msg'] == 'regret':
            res1 = QMessageBox.information(self,"是否悔棋","是否同意悔棋",QMessageBox.Yes|QMessageBox.No)
            print(res1)
            if res1 == QMessageBox.Yes:
                super().regret()
                data = {
                    'msg':'res1',
                    'res_type':'regret',
                    'res_data':'yes'
                }
                # self.chessmanColor= not self.chessmanColor
                self.isOwnflag =False
                self.netObject.send(json.dumps(data))
            else:
                data = {
                    'msg': 'res1',
                    'res_type': 'regret',
                    'res_data': 'no'
                }
                self.netObject.send(json.dumps(data))
        elif data['msg'] == 'res1':
            if data['res_type'] == 'regret':
                if data['res_data'] == 'yes':
                    super().regret()
                    # self.chessmanColor = not self.chessmanColor
                    self.isOwnflag = True
                else:
                    QMessageBox.information(self,"提示","对方拒绝",QMessageBox.Close)
        elif data['msg'] == 'lose':
            super().losegame()
            QMessageBox.information(self,"提示","对方认输",QMessageBox.Close)
        #     print(res2)
        #     data = {
        #             'msg':'res2',
        #             'res_type':'lose'
        #         }
        #     # self.isOwnflag =False
        # elif data['msg'] == 'res2':
        #     if data['res_type'] == 'lose':
        #         super().regret()


    def startgame(self):
        data = {'msg':'start' }
        self.netObject.send(json.dumps(data))
    def regret(self):
        if self.isOwnflag:
            return
        data = { 'msg':'regret'}
        self.netObject.send(json.dumps(data))
    def losegame(self):
        super().losegame()
        data = {'msg':'lose'}
        self.netObject.send(json.dumps(data))
        QMessageBox.information(self,"提示","你已认输",QMessageBox.Close)


    def autoChess(self,x,y):
        self.chessmanColor = not self.chessmanColor
        self.chessman =Chessman(color =self.chessmanColor,parent=self)
        self.chessman.x_index = x
        self.chessman.y_index = y
        self.chessman.move(x*30 +50-15,y*30 +50-15)
        self.chessman.show()
        self.chessboard[y][x] = self.chessman
        self.record.append(self.chessman)
        self.isWin(self.chessman)
        self.isOwnflag =not self.isOwnflag

    def mousePressEvent(self,event:PySide2.QtGui.QMouseEvent):
        if not self.isOwnflag:
            return
        if not self.xiaqiflag:
            return
        if super().mousePressEvent(event):
            # super().chessman
            x_index= self.chessman.x_index
            y_index= self.chessman.y_index
            data = {
                'msg':'position',
                'x': x_index ,
                'y': y_index
            }
            self.netObject.send(json.dumps(data)) #封装后 发送
            self.isOwnflag =not self.isOwnflag


#服务器
class NetClient(QObject):
    msg_signal = Signal(str)
    def __init__(self,ip,port,name):
        super().__init__()
        self.ip =ip
        self.port = int(port)
        self.name = name
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    def netConnect(self):
        try:
            self.socket.connect((self.ip,self.port))
        except Exception as e:
            QMessageBox.warning(None,'错误',str(e),QMessageBox.Close)
            return
        th = threading.Thread(target=self.recv)
        th.setDaemon(True)
        th.start()

    def recv(self):
        while True:
            try:
                # 01010101
                data = self.socket.recv(4096).decode()  #把二进制数解码成字符串类型，默认UTF-8
                self.msg_signal.emit(data)
            except Exception as e:
                QMessageBox.warning(None,'错误',str(e),QMessageBox.Close)
                break
    def send(self,data):
        self.socket.send(data.encode())  #编码 字符转字节类型

#客户端
class NetServer(QObject):

    msg_signal = Signal(str)
    def __init__(self,ip,port,name):
        super().__init__()
        self.ip =ip
        self.port = int(port)
        self.name = name
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    def netConnect(self):
        try:
            self.socket.bind(('',self.port)) # 绑定ip和端口号
            self.socket.listen(1)
        except Exception as e:
            print(e)
            return
        th = threading.Thread(target=self.recv)
        th.setDaemon(True)
        th.start()

    def recv(self):
        self.client_sock,addr = self.socket.accept()
        while True:
            try:
                data = self.client_sock.recv(4096)
                data = data.decode()
                #处理
                # print(data)
                self.msg_signal.emit(data)
            except Exception as e:
                print(e)
                break

    def send(self,data):
        if self.client_sock:
            self.client_sock.send(data.encode()) # 编码 字符转字节类型
