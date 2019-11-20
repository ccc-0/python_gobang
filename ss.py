def isWin(self, chessman):
    # 记录判断起始位置
    x = chessman.x_index
    y = chessman.y_index
    # 当前棋子记录颜色
    color = chessman.color

    def panduan(xcof, ycof):
        # 计数器
        count = 1
        x = chessman.x_index
        y = chessman.y_index
        while (x < 18 and x >= 0) and (y < 18 and y >= 0):
            if self.chessboard[y + ycof][x + xcof] and self.chessboard[y + ycof][x + xcof].color == color:
                count += 1
                y += ycof
                x += xcof
            else:
                break
            # 如果有5个相连的棋子则为赢
            if count == 5:
                self.whowin = win(self.chessmanColor, parent=self)
                self.whowin.move(60, 50)
                self.whowin.show()
                self.wintu.append(self.whowin)
                self.xiaqiflag = False
                self.whowinflag = True
                self.huiqiflag = True
        x = chessman.x_index
        y = chessman.y_index
        while (x < 18 and x >= 0) and (y < 18 and y >= 0):
            if self.chessboard[y - ycof][x - xcof] and self.chessboard[y - ycof][x - xcof].color == color:
                count += 1
                y -= ycof
                x -= xcof
            else:
                break
            if count == 5:
                self.whowin = win(self.chessmanColor, parent=self)
                self.whowin.move(60, 50)
                self.whowin.show()
                self.wintu.append(self.whowin)
                self.xiaqiflag = False
                self.whowinflag = True
                self.huiqiflag = True

    if x < 18 or x >= 0 or y < 18 or y >= 0:
        # 捺
        panduan(-1, -1)
        panduan(+1, +1)
        # 撇
        panduan(-1, +1)
        panduan(+1, -1)
        # 竖
        panduan(0, -1)
        panduan(0, +1)
        # 横
        panduan(-1, 0)
        panduan(+1, 0)

    def teshu1(xcof, ycof):
        count = 1
        x = chessman.x_index
        y = chessman.y_index
        while x == 18 and y != 18:
            if self.chessboard[y + ycof][x + xcof] and self.chessboard[y + ycof][x + xcof].color == color:
                count += 1
                y += ycof
                x += xcof
            else:
                break
            if count == 5:
                self.whowin = win(self.chessmanColor, parent=self)
                self.whowin.move(60, 50)
                self.whowin.show()
                self.wintu.append(self.whowin)
                self.xiaqiflag = False
                self.whowinflag = True
                self.huiqiflag = True
        x = chessman.x_index
        y = chessman.y_index
        while x == 18 and y != 18:
            if self.chessboard[y - ycof][x - xcof] and self.chessboard[y - ycof][x - xcof].color == color:
                count += 1
                y -= ycof
                x -= xcof
            else:
                break
            if count == 5:
                self.whowin = win(self.chessmanColor, parent=self)
                self.whowin.move(60, 50)
                self.whowin.show()
                self.wintu.append(self.whowin)
                self.xiaqiflag = False
                self.whowinflag = True
                self.huiqiflag = True

    def teshu2(xcof, ycof):
        count = 1
        x = chessman.x_index
        y = chessman.y_index
        while x == 18 and y != 18:
            if self.chessboard[y + ycof][x + xcof] and self.chessboard[y + ycof][x + xcof].color == color:
                count += 1
                y += ycof
                x += xcof
            while (x < 18 and x >= 0) and (y < 18 and y >= 0):
                if self.chessboard[y + ycof][x + xcof] and self.chessboard[y + ycof][x + xcof].color == color:
                    count += 1
                    y += ycof
                    x += xcof
                else:
                    break
                if count == 5:
                    self.whowin = win(self.chessmanColor, parent=self)
                    self.whowin.move(60, 50)
                    self.whowin.show()
                    self.wintu.append(self.whowin)
                    self.xiaqiflag = False
                    self.whowinflag = True
                    self.huiqiflag = True
            else:
                break

    if x == 18 and y != 18:
        teshu1(0, +1)
        teshu1(0, -1)
        teshu2(-1, 0)
        teshu2(-1, -1)
        teshu2(-1, +1)

    def teshu3(xcof, ycof):
        count = 1
        x = chessman.x_index
        y = chessman.y_index
        while y == 18 and x != 18:
            if self.chessboard[y + ycof][x + xcof] and self.chessboard[y + ycof][x + xcof].color == color:
                count += 1
                y += ycof
                x += xcof
            else:
                break
            if count == 5:
                self.whowin = win(self.chessmanColor, parent=self)
                self.whowin.move(60, 50)
                self.whowin.show()
                self.wintu.append(self.whowin)
                self.xiaqiflag = False
                self.whowinflag = True
                self.huiqiflag = True

        x = chessman.x_index
        y = chessman.y_index
        while y == 18 and x != 18:
            if self.chessboard[y - ycof][x - xcof] and self.chessboard[y - ycof][x - xcof].color == color:
                count += 1
                y -= ycof
                x -= xcof
            else:
                break
            if count == 5:
                self.whowin = win(self.chessmanColor, parent=self)
                self.whowin.move(60, 50)
                self.whowin.show()
                self.wintu.append(self.whowin)
                self.xiaqiflag = False
                self.whowinflag = True
                self.huiqiflag = True

    def teshu4(xcof, ycof):
        count = 1
        x = chessman.x_index
        y = chessman.y_index
        while y == 18 and x != 18:
            if self.chessboard[y + ycof][x + xcof] and self.chessboard[y + ycof][x + xcof].color == color:
                count += 1
                y += ycof
                x += xcof
                while (x < 18 and x >= 0) and (y < 18 and y >= 0):
                    if self.chessboard[y + ycof][x + xcof] and self.chessboard[y + ycof][x + xcof].color == color:
                        count += 1
                        y += ycof
                        x += xcof
                    else:
                        break
                    if count == 5:
                        self.whowin = win(self.chessmanColor, parent=self)
                        self.whowin.move(60, 50)
                        self.whowin.show()
                        self.wintu.append(self.whowin)
                        self.xiaqiflag = False
                        self.whowinflag = True
                        self.huiqiflag = True
            else:
                break

    if y == 18 and x != 18:
        teshu3(+1, 0)
        teshu3(-1, 0)
        teshu4(0, -1)
        teshu4(-1, -1)
        teshu4(+1, -1)

    def teshu5(xcof, ycof):
        count = 1
        x = chessman.x_index
        y = chessman.y_index
        while y == 18 and x == 18:
            if self.chessboard[y + ycof][x + xcof] and self.chessboard[y + ycof][x + xcof].color == color:
                count += 1
                y += ycof
                x += xcof
                while (x < 18 and x >= 0) and (y < 18 and y >= 0):
                    if self.chessboard[y + ycof][x + xcof] and self.chessboard[y + ycof][x + xcof].color == color:
                        count += 1
                        y += ycof
                        x += xcof
                    else:
                        break
                    if count == 5:
                        self.whowin = win(self.chessmanColor, parent=self)
                        self.whowin.move(60, 50)
                        self.whowin.show()
                        self.wintu.append(self.whowin)
                        self.xiaqiflag = False
                        self.whowinflag = True
                        self.huiqiflag = True
                while (x < 18 and x >= 0) and y == 18:
                    if self.chessboard[y + ycof][x + xcof] and self.chessboard[y + ycof][x + xcof].color == color:
                        count += 1
                        y += ycof
                        x += xcof
                    else:
                        break
                    if count == 5:
                        self.whowin = win(self.chessmanColor, parent=self)
                        self.whowin.move(60, 50)
                        self.whowin.show()
                        self.wintu.append(self.whowin)
                        self.xiaqiflag = False
                        self.whowinflag = True
                        self.huiqiflag = True
                while x == 18 and (y < 18 and y >= 0):
                    if self.chessboard[y + ycof][x + xcof] and self.chessboard[y + ycof][x + xcof].color == color:
                        count += 1
                        y += ycof
                        x += xcof
                    else:
                        break
                    if count == 5:
                        self.whowin = win(self.chessmanColor, parent=self)
                        self.whowin.move(60, 50)
                        self.whowin.show()
                        self.wintu.append(self.whowin)
                        self.xiaqiflag = False
                        self.whowinflag = True
                        self.huiqiflag = True
            else:
                break

    if x == 18 and y == 18:
        teshu5(-1, -1)
        teshu5(-1, 0)
        teshu5(0, -1)

