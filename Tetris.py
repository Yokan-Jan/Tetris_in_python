#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import random
import sys
import os
import copy
import math
import msvcrt

class CTetris():
    tplShape = ('straight', 'square', 'Z-shape',
                'S-shape', 'L-shape', 'J-shape', 'T-shape')
    dctShape_map = {
        tplShape[0]: [[1, 1, 1, 1]],
        tplShape[1]: [[1, 1], [1, 1]],
        tplShape[2]: [[1, 1, 0], [0, 1, 1]],
        tplShape[3]: [[0, 1, 1], [1, 1, 0]],
        tplShape[4]: [[0, 0, 1], [1, 1, 1]],
        tplShape[5]: [[1, 0, 0], [1, 1, 1]],
        tplShape[6]: [[1, 1, 1], [0, 1, 0]],
    }
    m_nextShape = None
    lstBoard = []
    m_row = 20
    m_col = 12
    # 初始化


    def __init__(self):
        self.CreateBoard()
        self.CreateList()
        self.m_point = 0
    # 生成一个绘板，用于打印


    def CreateBoard(self):
        for i in range(CTetris.m_row):
            self.lstBoard.append([])
            for j in range(CTetris.m_col):
                if j == 0 or j == CTetris.m_col - 1 or i == 0 or i == CTetris.m_row - 1:
                    self.lstBoard[i].append(1)
                else:
                    self.lstBoard[i].append(0)

    # 生成两个列表，一个用于存储当前方块，一个用于存储落下方块


    def CreateList(self):
        self.lstCurr = []
        self.lstSure = []

    # 随机生成一个方块，并且居中生成。


    def CreateShape(self):
        self.m_nextShape = self.dctShape_map[
            self.tplShape[random.randint(0, len(self.tplShape) - 1)]]
        self.iShapeWidth = len(self.m_nextShape)

        for i in range(self.iShapeWidth):
            self.iShapeLength = len(self.m_nextShape[i])
            self.iDistoLeft = (CTetris.m_col - self.iShapeLength) / 2
            for j in range(self.iShapeLength):
                if self.m_nextShape[i][j] == 1:
                    self.lstCurr.append([i + 1, j + self.iDistoLeft])
    # 获得当前方块的位置


    def GetCur(self):
        for item in self.lstCurr:
            x = item[0]
            y = item[1]
            self.lstBoard[x][y] = 2

    # 获得已落下方块的位置


    def GetSure(self):
        for item in self.lstSure:
            x = item[0]
            y = item[1]
            self.lstBoard[x][y] = 2
    # 绘制函数


    def RenderGame(self):
        self.GetCur()
        self.GetSure()
        for i in range(CTetris.m_row):
            for j in range(CTetris.m_col):
                if self.lstBoard[i][j] == 1:
                    print '/',
                elif self.lstBoard[i][j] == 2:
                    print '@',
                else:
                    print ' ',
            print ''
        print('Your Score is: ' + str(self.m_point)).center(20)
    # 直接落下


    def ShapeFallDown(self):
        while self.CheckDown():
            self.ShapeMoveDown()

    # 慢慢落下


    def ShapeMoveDown(self):
        for item in self.lstCurr:
            x = item[0]
            y = item[1]
            self.lstBoard[x][y] = 0
        if self.CheckDown() == True:
            for item in self.lstCurr:
                if(item[0] < 18):
                    item[0] += 1
                else:
                    break
        else:
            self.SaveData()

    # 左移


    def ShapeMoveLeft(self):
        if self.CheckLeft() == True:
            for item in self.lstCurr:
                x = item[0]
                y = item[1]
                self.lstBoard[x][y] = 0
                if(item[1] > 1):
                    item[1] -= 1

    # 右移


    def ShapeMoveRight(self):
        if self.CheckRight() == True:
            for item in self.lstCurr:
                x = item[0]
                y = item[1]
                self.lstBoard[x][y] = 0
                item[1] += 1
    # 是否可以往下移动


    def CheckDown(self):
        lstTemp = copy.deepcopy(self.lstCurr)
        for item in lstTemp:
            item[0] += 1
        for item in lstTemp:
            if item in self.lstSure or item[0] > 18:
                return False
        return True
    # 是否可以向右移动


    def CheckRight(self):
        lstTemp = copy.deepcopy(self.lstCurr)
        for item in lstTemp:
            item[1] += 1
        for item in lstTemp:
            if item in self.lstSure or item[1] > 10:
                return False
        return True
    # 是否可以向左移动


    def CheckLeft(self):
        lstTemp = copy.deepcopy(self.lstCurr)
        for item in lstTemp:
            item[1] -= 1
        for item in lstTemp:
            if item in self.lstSure or item[1] < 1:
                return False
        return True
    # 当前位置是否可以旋转


    def CheckRotate(self):
        lstTemp = copy.deepcopy(self.lstCurr)
        rot_x = lstTemp[2][0]
        rot_y = lstTemp[2][1]
        for item in lstTemp:
            y = rot_y + (item[0] - rot_x) * 1 + (item[1] - rot_y) * 0
            x = rot_x + (item[0] - rot_x) * 0 - (item[1] - rot_y) * 1
            item[0], item[1] = x, y
        for item in lstTemp:
            if item in self.lstSure or self.lstBoard[item[0]][item[1]] == 1:
                return False
        return True
    # 旋转方块


    def RotateShape(self):
        if self.CheckRotate():
            for item in self.lstCurr:
                x = item[0]
                y = item[1]
                self.lstBoard[x][y] = 0

            rot_x = self.lstCurr[-1][0]
            rot_y = self.lstCurr[-1][1]
            for item in self.lstCurr:
                y = rot_y + (item[0] - rot_x) * 1 + (item[1] - rot_y) * 0
                x = rot_x + (item[0] - rot_x) * 0 - (item[1] - rot_y) * 1
                item[0], item[1] = x, y

    # 方块操作


    def MoveShape(self):
        input = msvcrt.getch()
        if input == 's':
            self.ShapeMoveDown()
        elif input == 'a':
            self.ShapeMoveLeft()
        elif input == 'd':
            self.ShapeMoveRight()
        elif input == 'w':
            self.RotateShape()
        elif input == 'f':
            self.ShapeFallDown()
            self.SaveData()
        # elif input == 't':
            # self.test()

    # 测试用


    def test(self):
        for item in self.lstSure:
            if item[0] < 18:
                self.clear()
                item[0] += 1

    # 保存落下后的方块，更新下一个方块


    def SaveData(self):
        for item in self.lstCurr:
            self.lstSure.append(item)
        self.Eliminate()
        self.lstCurr = []
        self.CreateShape()

    # 消除装满的一层


    def Eliminate(self):
        #self.lstSure.sort(reverse = True)
        for i in range(1, 19):
            iCount = 0
            for item in self.lstSure:
                if item[0] == i:
                    iCount += 1
            if iCount == 10:
                self.AllDown(i)
                self.m_point += 1

    # 让消除的那层，上面的所有层数下降


    def AllDown(self, flag):
        tmpList = []
        for item in self.lstSure:
            if item[0] == flag:
                tmpList.append(item)

        for item in tmpList:
            self.lstSure.remove(item)
            self.lstBoard[item[0]][item[1]] = 0

        for item in self.lstSure:
            if item[0] < flag:
                self.clear()
                item[0] += 1

        # 测试用的
    def clear(self):
        for i in range(CTetris.m_row):
            for j in range(CTetris.m_col):
                if j == 0 or j == CTetris.m_col - 1 or i == 0 or i == CTetris.m_row - 1:
                    continue
                else:
                    self.lstBoard[i][j] = 0
    # 检测是否会失败


    def GetLose(self):
        for item in self.lstCurr:
            if item in self.lstSure:
                print ' You are lose, man!!!'
                time.sleep(2)
                sys.exit()

    # 开始游戏
    def Start(self):
        self.CreateShape()
        self.RenderGame()
        self.MainLoop()
    # 刷新

    def flush(self):
        #self.lstCurr = []
        self.RenderGame()
    # 游戏主循环

    def MainLoop(self):
        while True:
            self.MoveShape()
            # time.sleep(0.05)
            os.system('cls')
            self.GetLose()
            self.RenderGame()

def main():
    game = CTetris()
    game.Start()

if __name__ == '__main__':
    main()
