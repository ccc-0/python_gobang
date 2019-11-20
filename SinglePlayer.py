from DoublePlayer import *
import os,PySide2,sys

dirname = os.path.dirname(PySide2.__file__)
plugin_path = os.path.join(dirname, 'plugins', 'platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path

class Singlewindow(Doublewindow):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setWindowTitle('人机对战')

    def mousePressEvent(self,event:PySide2.QtGui.QMouseEvent):
        x = event.x()
        y = event.y()
        self.chessman = Chessman(self.chessmanColor,parent=self)
        x,y= self.chessman.getindex(x,y)
        if self.chessboard[self.chessman.y_index][self.chessman.x_index]==None:
            super().mousePressEvent(event)
            if self.xiaqiflag == True:
                if x < 50-15 or x > 590+15:
                    return
                if y < 50-15 or y > 590+15:
                    return
                # if self.chessboard[self.chessman.y_index][self.chessman.x_index]==None:
                self.autoPlay()
                    # self.zz.append(self.chessman)
        # else :
            # self.chessman.deleteLater()
            # self.chessmanColor = not self.chessmanColor


    def autoPlay(self):
        #获取一个棋子，执行下棋操作
        self.chessmanColor = not self.chessmanColor
        self.chessman = self.getAutoChess()
        x = self.chessman.x_index *30 +50-15
        y = self.chessman.y_index *30 +50-15
        self.chessman.move(x,y)
        self.chessman.show()
        self.chessboard[self.chessman.y_index][self.chessman.x_index]= self.chessman
        self.record.append(self.chessman)
        self.isWin(self.chessman)

    #AI算法
    def getAutoChess(self):
        #获取棋盘上所有白子分数
        #获取棋盘上所有黑子分数
        #取他们最大值
        w_score = []
        b_score =[]
        #白棋
        for i in range(19):
            for j in range(19):
                if self.chessboard[i][j]:
                    w_score.append(0)
                else:
                    # self.chessboard[i][j] =Chessman(1,self)
                    w_score.append(self.getScore(i,j,1))
                    # tmp =  self.chessboard[i][j]
                    # self.chessboard[i][j] = None
                    # del tmp
        #黑棋
        for i in range(19):
            for j in range(19):
                if self.chessboard[i][j]:
                    b_score.append(0)
                else:
                    # self.chessboard[i][j] =Chessman(0,self)
                    b_score.append(self.getScore(i,j,0))
                    # del self.chessboard[i][j]
                    # self.chessboard[i][j] = None

        tmp = [ max(x,y) for x,y in zip (w_score,b_score)] #两黑白数组对比取最大
        res = tmp.index( max(tmp))
        x_index = res % 19
        y_index = res //19
        c = Chessman(self.chessmanColor,parent=self)
        c.x_index = x_index
        c.y_index = y_index
        return c
    def getScore(self,i,j,color):
        color = color
        score = [0,0,0,0]
        y = i
        x = j
        #遍历四个放向，计算棋子分数
        #上 y-1 x=0
        for c in range(4):
            if y-1 <0:
                break
            if self.chessboard[y-1][x] and self.chessboard[y-1][x].color == color:
                score[0] +=1
            else:
                break
            y-=1
        #下 y+1
        y = i
        for c in range(4):
            if y+1 >18:
                break
            if self.chessboard[y+1][x]and self.chessboard[y+1][x].color == color:
                score[0] +=1
            else:
                break
            y+=1
        #左右
        x=j
        y=i
        #左 y+0 x-1
        for c in range(4):
            if x-1 <0:
                break
            if self.chessboard[y][x-1] and self.chessboard[y][x-1].color == color:
                score[1] +=1
            else:
                break
            x-=1
        #右 y+0 x+1
        x = j
        for c in range(4):
            if x+1 >18:
                break
            if self.chessboard[y][x+1]and self.chessboard[y][x+1].color == color:
                score[1] +=1
            else:
                break
            x+=1
        #左斜
        x=j
        y=i
        #左上 y-1 x-1
        for c in range(4):
            if y-1<0 or x-1<0:
                break
            if self.chessboard[y-1][x-1] and self.chessboard[y-1][x-1].color == color:
                score[2] +=1
            else:
                break
            x-=1
            y-=1
        #右下
        y = i
        x = j
        for c in range(4):
            if y+1>18 or x+1>18 :
                break
            if self.chessboard[y+1][x+1]and self.chessboard[y+1][x+1].color == color:
                score[2] +=1
            else:
                break
            y+=1
            x+=1
        #右斜
        y=i
        x=j
        #右上 y-1 x+1
        for c in range(4):
            if y-1<0 or x+1>18:
                break
            if self.chessboard[y-1][x+1] and self.chessboard[y-1][x+1].color == color:
                score[3] +=1
            else:
                break
            x+=1
            y-=1
        #右下 y+1 x-1
        y = i
        x = j
        for c in range(4):
            if y+1>18 or x-1<0 :
                break
            if self.chessboard[y+1][x-1]and self.chessboard[y+1][x-1].color == color:
                score[3] +=1
            else:
                break
            y+=1
            x-=1
        return max(score)

    def regret(self):
        super().regret()
        super().regret()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Singlewindow()
    w.show()
    sys.exit(app.exec_())

