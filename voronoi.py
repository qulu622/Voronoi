# M063040030 劉珊如 (Shan-Ru Liu)
# $LAN=PYTHON$
# -------------------------------------------------------------------------------------------

from tkinter import *
from tkinter.ttk import *
import math

#各種class
class Dot(object):
    def __init__(self, x, y, name):
        self.x = x
        self.y = y
        self.name = name

class Line(object):
    def __init__(self, x1, y1, x2, y2, bx1, by1, bx2, by2, name, isRay, where):
        self.x1 = x1 #端點1 x
        self.y1 = y1 #端點1 y
        self.x2 = x2 #端點2 x
        self.y2 = y2 #端點2 y

        #由哪兩個點畫出來的 bx1,by1,bx2,by2
        self.bx1 = bx1 
        self.by1 = by1
        self.bx2 = bx2
        self.by2 = by2
        
        self.name = name #id: name
        self.isRay = isRay #是否為射線 isRay  t or f
        self.where = where #左or右orHP where, left right center

class LineAndInterY(object):
    def __init__(self, x1, y1, x2, y2, bx1, by1, bx2, by2, name, isRay, where, interY):
        self.x1 = x1 #端點1 x
        self.y1 = y1 #端點1 y
        self.x2 = x2 #端點2 x
        self.y2 = y2 #端點2 y

        #由哪兩個點畫出來的 bx1,by1,bx2,by2
        self.bx1 = bx1 
        self.by1 = by1
        self.bx2 = bx2
        self.by2 = by2
        
        self.name = name #id: name
        self.isRay = isRay #是否為射線 isRay  t or f
        self.where = where #左or右orHP where, left right center
        self.interY = interY #與xbound的交點, y座標

#讀檔
def GetTest(fIn,tmp):
    get = tmp
    while get == '#' or get == ' ' or get == '\n':
        if (get != '\n'):
            fIn.readline()
        get = fIn.read(1)
    get = get + fIn.readline()
    return int(get)

def GetNum(fIn):
    get = ''
    num = fIn.read(1)
    while num != ' ' and num != '\n':
        get = get + num
        num = fIn.read(1)
    return int(get)

def ReadData(event):
    ClearDraw(event)
    tmp = fIn.read(1)
    if ( tmp == 'P' ): #讀回output檔
        while tmp != '':
            if ( tmp == 'P' ): 
                fIn.read(1) #讀空白
                x = GetNum(fIn)
                y = GetNum(fIn)
                dotList.append(Dot(x,y,math.inf))
                listbox.insert(END, str(len(dotList)) + '  :   (' + str(x) + ',' + str(y) + ')')
                c.create_oval(x, y, x, y, width=3, fill=Color())
            else: # tmp == E
                fIn.read(1) #讀空白
                x1 = GetNum(fIn)
                y1 = GetNum(fIn)
                x2 = GetNum(fIn)
                y2 = GetNum(fIn)
                vorLineList.append(Line(x1,y1,x2,y2,0, 0, 0, 0, math.inf, 't', 'all'))
                listbox.insert(END, str(len(vorLineList)) + '  :   (' + str(x1) + ',' + str(y1) + ') '
                               + '(' + str(x2) + ',' + str(y2) + ') ' )
                c.create_line(x1, y1, x2, y2, width=3, fill=Color())
            tmp = fIn.read(1)
    else: #讀測資
        test = GetTest(fIn,tmp) #排除註解,讀到第一個數字
        if test != 0:
            n = test
            while n != 0:
                x = GetNum(fIn)
                y = GetNum(fIn)
                n = n - 1
                ReadDraw(x,y)
        else:
            print('讀入點數為零，檔案測試停止')

def ReadFile(event):
    s = entry.get()
    global fIn
    fIn = open(s + '.txt', 'r')
    ReadData(event)

#畫布
def MouseDraw(event):
    listbox.insert(END, str(len(dotList)) + '  :   (' + str(event.x) + ',' + str(event.y) + ')')
    name = c.create_oval(event.x, event.y, event.x, event.y, width=3, outline=Color())
    dotList.append(Dot(event.x,event.y,name))

def ReadDraw(x,y):
    listbox.insert(END, str(len(dotList)) + '  :   (' + str(x) + ',' + str(y) + ')')
    name = c.create_oval(x, y, x, y, width=3, outline=Color())
    dotList.append(Dot(x,y,name))

def ClearDraw(event):
    c.delete('all')
    listbox.delete(0,END)
    dotList.clear()
    vorLineList.clear()
    global step
    step = 0
    global xdir
    xdir = 'center'
    global xbound
    xbound = 0
    leftDotList.clear()
    rightDotList.clear()

#計算
def Color(): #處理顏色
    if (xdir == 'center'):
        return 'black'
    if (xdir == 'left'):
        return '#cc33ff'
    elif (xdir == 'right'):
        return '#ff9933'
    
def Limit(outX,outY,vecX,vecY): #處理超出邊界問題
    tmpx = outX
    tmpy = outY

    leftbound = 0
    rightbound = 600

    #if ( xdir == 'left' ):
        #rightbound = xbound
    #elif ( xdir == 'right' ):
        #leftbound = xbound
        
        
    if (vecX >= 0 and vecY >= 0):
        while (tmpx < rightbound and tmpy < 600):
            tmpx = tmpx+vecX
            tmpy = tmpy+vecY
    elif(vecX >= 0 and vecY < 0):
        while (tmpx < rightbound and tmpy >= 0):
            tmpx = tmpx+vecX
            tmpy = tmpy+vecY
    elif(vecX < 0 and vecY >= 0):
        while (tmpx >= leftbound and tmpy < 600):
            tmpx = tmpx+vecX
            tmpy = tmpy+vecY
    else: # vecX < 0 and vecY < 0
        while (tmpx >= leftbound and tmpy >= 0):
            tmpx = tmpx+vecX
            tmpy = tmpy+vecY
    
    return tmpx,tmpy
    
def DrawLineForTri(outX, outY, midx, midy, cos, x, y, bx1, by1, bx2, by2): #有大概處理超出邊界的問題
    if ( cos > 0  ): #銳
        #print('銳\n')
        vecX = midx - outX
        vecY = midy - outY
        tmpx,tmpy = Limit(outX,outY,vecX,vecY)
        #tmpx = outX + 1200*vecX
        #tmpy = outY + 1200*vecY
    elif ( cos == 0 ): #直
        #print('直\n')
        vecX = midx - x
        vecY = midy - y
        tmpx,tmpy = Limit(outX,outY,vecX,vecY)
        #tmpx = outX + 1200*vecX
        #tmpy = outY + 1200*vecY
    else: # cos < 0 , 鈍
        #print('鈍\n')
        vecX = outX - midx
        vecY = outY - midy
        tmpx,tmpy = Limit(outX,outY,vecX,vecY)
        #tmpx = outX + 1200*vecX
        #tmpy = outY + 1200*vecY
        
    tmpList = [Dot(outX,outY,math.inf),Dot(tmpx,tmpy,math.inf)]
    tmpList.sort(key = lambda l:(l.x,l.y))
    name = c.create_line(outX, outY, tmpx, tmpy, width=3, fill=Color())
    #x1, y1, x2, y2, bx1, by1, bx2, by2, name, isRay, m, where
    vorLineList.append(Line(tmpList[0].x,tmpList[0].y,tmpList[1].x,tmpList[1].y,
                            bx1, by1, bx2, by2, name, 't', xdir)) 
    
def DrawLine(x1,y1,x2,y2): #給兩個點,畫一條中垂線,已處理超出邊界問題
    leftbound = 0
    rightbound = 600

    #if ( xdir == 'left' ):
        #rightbound = xbound
    #elif ( xdir == 'right' ):
        #leftbound = xbound
    
    if(y1 != y2 and x1 != x2):
        m1 = (y1-y2)/(x1-x2) #斜率
    else: #平行於x軸 or y軸
        if ( y1 == y2 ):
            m1 = math.inf
        else:
            m1 = 0

    if (m1 != 0 and m1 != math.inf):
        m2 = -1/m1 #垂直線的斜率
        midx = (x1+x2)/2 #中點x
        midy = (y1+y2)/2 #中點y
        b = midy-(m2*midx) #截距?

        t1x = leftbound
        t1y = (m2*t1x)+b
        t2x = rightbound
        t2y = (m2*t2x)+b
        
        t3y = 0
        t3x = (t3y-b)/m2
        t4y = 600
        t4x = (t4y-b)/m2

        num = 0
        if ( t1y >= 0 and t1y <= 600 ): # t1x = leftbound
            d1x = t1x
            d1y = t1y
            num = num+1
        if ( t2y >= 0 and t2y <= 600 ): # t2x = rightbound
            if ( num == 0 ):
                d1x = t2x
                d1y = t2y
                num = num+1
            else:
                d2x = t2x
                d2y = t2y
        if ( t3x >= leftbound and t3x <= rightbound ): # t3y = 0
            if ( num == 0 ):
                d1x = t3x
                d1y = t3y
                num = num+1
            else:
                d2x = t3x
                d2y = t3y
        if ( t4x >= leftbound and t4x <= rightbound ):  # t4y = 600
            d2x = t4x
            d2y = t4y            
    else:
        if ((x1-x2) == 0): # x1 = x2
            tmpy = (y1+y2)/2
            d1x = leftbound
            d1y = tmpy
            d2x = rightbound
            d2y = tmpy
        else: # y1 = y2
            tmpx = (x1+x2)/2
            d1x = tmpx
            d1y = 0
            d2x = tmpx
            d2y = 600

    tmpList = [Dot(d1x,d1y,math.inf),Dot(d2x,d2y,math.inf)] #'name' 
    tmpList.sort(key = lambda l:(l.x,l.y))
    
    name = c.create_line(d1x,d1y,d2x,d2y, width=3, fill=Color())
    #x1, y1, x2, y2, bx1, by1, bx2, by2, name, isRay, m, where
    vorLineList.append(Line(tmpList[0].x,tmpList[0].y,tmpList[1].x,tmpList[1].y,
                            x1, y1, x2, y2, name, 't', xdir))

def WhatCase(dotList): #三點共線,三角形
    x1 = dotList[0].x
    y1 = dotList[0].y
    x2 = dotList[1].x
    y2 = dotList[1].y
    x3 = dotList[2].x
    y3 = dotList[2].y
    
    if ( x1 == x2 and x2 == x3 ): #垂直
        return 1
    elif( y1 == y2 and y2 == y3 ): #水平
        return 1
    else:
        #dot2.3
        if ( y2 != y3 and x2 != x3 ):
            m1 = (y2-y3)/(x2-x3)
            mm1 = -1/m1 #垂直線的斜率
        else:
            if ( y2 == y3 ):
                m1 = 0
                mm1 = math.inf
            else:
                m1 = math.inf
                mm1 = 0

        midx1 = (x2+x3)/2 #中點x
        midy1 = (y2+y3)/2 #中點y
        b1 = midy1-(m1*midx1) #截距? 方程式
        bb1 = midy1-(mm1*midx1) #截距? 垂直線

        #dot3.1    
        if ( y3 != y1 and x3 != x1 ):
            m2 = (y3-y1)/(x3-x1)
            mm2 = -1/m2 #垂直線的斜率
        else:
            if ( y3 == y1 ):
                m2 = 0
                mm2 = math.inf
            else:
                m2 = math.inf
                mm2 = 0
            
        midx2 = (x3+x1)/2 #中點x
        midy2 = (y3+y1)/2 #中點y
        b2 = midy2-(m2*midx2) #截距? 方程式
        bb2 = midy2-(mm2*midx2) #截距? 垂直線

        #dot1.2         
        if ( y1 != y2 and x1 != x2 ):
            m3 = (y1-y2)/(x1-x2)
            mm3 = -1/m3 #垂直線的斜率       
        else:
            if ( y1 == y2 ):
                m3 = 0
                mm3 = math.inf
            else:
                m3 = math.inf
                mm3 = 0

        midx3 = (x1+x2)/2 #中點x
        midy3 = (y1+y2)/2 #中點y
        b3 = midy3-(m3*midx3) #截距? 方程式
        bb3 = midy3-(mm3*midx3) #截距? 垂直線

        if ( m1 == m2 and b1 == b2 ): #共線
            return 1
        else: #求外心
            if ( mm1 == math.inf ):
                outX = -((bb2-bb3)/(mm2-mm3)) #加負號, 因為程式的y軸方向與一般的相反, 斜率受影響
                outY = (mm2*outX)+bb2
            elif( mm2 == math.inf ):
                outX = -((bb1-bb3)/(mm1-mm3)) #加負號, 因為程式的y軸方向與一般的相反, 斜率受影響
                outY = (mm1*outX)+bb1
            else:
                outX = -((bb1-bb2)/(mm1-mm2)) #加負號, 因為程式的y軸方向與一般的相反, 斜率受影響
                outY = (mm2*outX)+bb2
            
            #計算三邊長
            side1 = math.sqrt(math.pow(x2-x3,2)+math.pow(y2-y3,2))
            side2 = math.sqrt(math.pow(x1-x3,2)+math.pow(y1-y3,2))
            side3 = math.sqrt(math.pow(x1-x2,2)+math.pow(y1-y2,2))

            #判斷角度>90? : >0,銳 =0,直角 <0,鈍角
            cos1 = (math.pow(side2,2)+math.pow(side3,2)-math.pow(side1,2))/(2*side2*side3)
            cos2 = (math.pow(side1,2)+math.pow(side3,2)-math.pow(side2,2))/(2*side1*side3)
            cos3 = (math.pow(side1,2)+math.pow(side2,2)-math.pow(side3,2))/(2*side1*side2)

            DrawLineForTri(outX, outY, midx1, midy1, cos1, x1, y1, x2, y2, x3, y3)
            DrawLineForTri(outX, outY, midx2, midy2, cos2, x2, y2, x1, y1, x3, y3)
            DrawLineForTri(outX, outY, midx3, midy3, cos3, x3, y3, x1, y1, x2, y2)
            
            #print('x: ' + str(int(outX)) + ', y: ' +str(int(outY))+ '\n')
            #c.create_oval(outX, outY, outX, outY, width=3, outline='red')    
        
    return 0

def RunButton(event):
    Run()

def Run():
    print('Run \n')
    global step
    i = step
    while ( i < 8 ):
        RunAStep()
        step = step+1
        i = step
    
def TwoDotVor(aList):
    DrawLine(aList[0].x,aList[0].y,aList[1].x,aList[1].y)
    
def ThreeDotVor(aList):
    case = WhatCase(aList)
    if (case == 1):
        DrawLine(aList[0].x,aList[0].y,aList[1].x,aList[1].y)
        DrawLine(aList[1].x,aList[1].y,aList[2].x,aList[2].y)

def TwoDotDis(x1,y1,x2,y2):
    return math.sqrt(math.pow(x1-x2,2)+math.pow(y1-y2,2))

def FindInterY(x1,y1,x2,y2):
    interY = -1
    
    m = 0
    if (y1 == y2 ):
        m = 0
    elif (x1 == x2 ):
        m = math.inf
    else:
        m = (y2-y1)/(x2-x1)
    
    if ( x1 <= xbound and x2 >= xbound ):
        b = y1-(m*x1)
        interY = m*xbound+b        
    return interY

def IsExist(aList,x,y):
    i = 0
    while ( i < len(aList) ):
        if ( aList[i].x == x and aList[i].y == y ):
            return 1
        i = i+1
    return 0

def FindInter(x11,y11,x12,y12,x21,y21,x22,y22):
    m1 = 0
    if ( y11 == y12 ):
        m1 = 0
    elif ( x11 == y12 ):
        m1 = math.inf
    else:
        m1 = (y12-y11)/(x12-x11)
    b1 = y11-(m1*x11)

    m2 = 0
    if ( y21 == y22 ):
        m2 = 0
    elif ( x21 == y22 ):
        m2 = math.inf
    else:
        m2 = (y22-y21)/(x22-x21)
    b2 = y21-(m2*x21)

    x = (b2-b1)/(m1-m2)
    y = m1*x+b1

    return x,y
    
def RunAStep():
    #print('Run A Step\n')
    global step
    global xdir
    global xbound_id
    global xbound
    global beforeLenVor
    global afterLenVor
    
    if (step == 0): #把所有點排序, 並檢查是否有重複的點, 之後將所有點分一半, 若小於4點則直接做
        print('step0\n')
        dotList.sort(key = lambda l:(l.x,l.y))
        for i in range(0,len(dotList)-1): #處理重複的點
            if ( dotList[i].x == dotList[i+1].x and dotList[i].y == dotList[i+1].y ):
                del dotList[i+1]
                         
        if (len(dotList) == 2):
            TwoDotVor(dotList)
        elif(len(dotList) == 3):
            ThreeDotVor(dotList)
        elif(len(dotList) > 3):
            i = 0
            half = len(dotList)/2
            if (len(dotList) % 2 == 1):
                xbound = (dotList[int(half)].x + dotList[int(half)+1].x)/2
            else:
                xbound = (dotList[int(half)-1].x + dotList[int(half)].x)/2

            xbound_id = c.create_line(xbound,0,xbound,600, width=3, fill='yellowgreen')
                
            while ( i < len(dotList) ): #把點分成左右兩個list
                if ( i < half ): #如果是奇數個點, 左邊會多一個點, 因為half會是x.5
                    leftDotList.append(Dot(dotList[i].x,dotList[i].y,dotList[i].name))
                    #leftDotList.sort(key = lambda l:(l.y,l.x))
                    xdir = 'left'
                    #c.create_oval(dotList[i].x, dotList[i].y, dotList[i].x, dotList[i].y, width=3, outline=Color()) #左邊 紫色
                    c.itemconfig(dotList[i].name, outline=Color())
                else:
                    rightDotList.append(Dot(dotList[i].x,dotList[i].y,dotList[i].name))
                    #rightDotList.sort(key = lambda l:(l.y,l.x))
                    xdir = 'right'
                    #c.create_oval(dotList[i].x, dotList[i].y, dotList[i].x, dotList[i].y, width=3, outline=Color()) #右邊 橘色
                    c.itemconfig(dotList[i].name, outline=Color())
                i = i+1
    elif (step == 1): #左邊voronoi
        xdir = 'left'
        if (len(leftDotList) == 2):
            TwoDotVor(leftDotList)
        elif(len(leftDotList) == 3): #大於3點先不做vor
            ThreeDotVor(leftDotList)
        print('step1\n')
    
    elif (step == 2): #右邊voronoi
        xdir = 'right'
        if (len(rightDotList) == 2):
            TwoDotVor(rightDotList)
        elif(len(rightDotList) == 3): #大於3點先不做vor
            ThreeDotVor(rightDotList)
        print('step2\n')
    elif (step == 3): #左邊convex hull
        xdir = 'left'
        i = 0
        while ( i < len(vorLineList) ):
            if ( vorLineList[i].where == xdir and vorLineList[i].isRay == 't' ):
                tmpList = [Dot(vorLineList[i].bx1,vorLineList[i].by1,math.inf),
                           Dot(vorLineList[i].bx2,vorLineList[i].by1,math.inf)] #'name'
                tmpList.sort(key = lambda l:(l.x,l.y))
                name = c.create_line(vorLineList[i].bx1,vorLineList[i].by1,vorLineList[i].bx2,vorLineList[i].by2,
                                     width=3, fill=Color())
                # m = (vorLineList[i].by1-vorLineList[i].by2)/(vorLineList[i].bx1-vorLineList[i].bx2) 應該不用紀錄
                conLineList.append(Line(tmpList[0].x,tmpList[0].y,tmpList[1].x,tmpList[1].y,
                                        tmpList[0].x,tmpList[0].y,tmpList[1].x,tmpList[1].y, name, 'f', xdir))
            i = i+1
        print('step3\n')
    elif (step == 4): #右邊convex hull
        xdir = 'right'
        i = 0
        while ( i < len(vorLineList) ):
            if ( vorLineList[i].where == xdir and vorLineList[i].isRay == 't' ):
                tmpList = [Dot(vorLineList[i].bx1,vorLineList[i].by1,math.inf),Dot(vorLineList[i].bx2,vorLineList[i].by1,math.inf)] #'name'
                tmpList.sort(key = lambda l:(l.x,l.y))
                name = c.create_line(vorLineList[i].bx1,vorLineList[i].by1,vorLineList[i].bx2,vorLineList[i].by2,
                                     width=3, fill=Color())
                #m = (vorLineList[i].by1-vorLineList[i].by2)/(vorLineList[i].bx1-vorLineList[i].bx2) 應該不用紀錄
                conLineList.append(Line(tmpList[0].x,tmpList[0].y,tmpList[1].x,tmpList[1].y,
                                        tmpList[0].x,tmpList[0].y,tmpList[1].x,tmpList[1].y, name, 'f', xdir))
            i = i+1
        print('step4\n')
    elif (step == 5): #HP, 刪除多餘的線, 完成voronoi的合併
        xdir = 'center'
        i = 0
        hpLineList = []
        hpLeftDotList = []
        hpRightDotList = []
        count = 0
        while ( i < len(vorLineList) ):
            interY = FindInterY(vorLineList[i].x1,vorLineList[i].y1,vorLineList[i].x2,vorLineList[i].y2)
            if ( interY >=0 and interY <= 600 ):
                count = count+1
                #c.create_oval(xbound, interY, xbound, interY, width=3, outline=Color())
                hpLineList.append(LineAndInterY(vorLineList[i].x1,vorLineList[i].y1,vorLineList[i].x2,vorLineList[i].y2,
                                  vorLineList[i].bx1,vorLineList[i].by1,vorLineList[i].bx2,vorLineList[i].by2,
                                  vorLineList[i].name, vorLineList[i].isRay, vorLineList[i].where, interY))
                
                if ( vorLineList[i].where == 'left' ):
                    if ( IsExist(hpLeftDotList,vorLineList[i].bx1,vorLineList[i].by1) == 0 ):
                        hpLeftDotList.append(Dot(vorLineList[i].bx1,vorLineList[i].by1,math.inf))
                        #print('left b1,dot\n')
                    if ( IsExist(hpLeftDotList,vorLineList[i].bx2,vorLineList[i].by2) == 0 ):
                        hpLeftDotList.append(Dot(vorLineList[i].bx2,vorLineList[i].by2,math.inf))
                        #print('left b2,dot\n')
                else:
                    if ( IsExist(hpRightDotList,vorLineList[i].bx1,vorLineList[i].by1) == 0 ):
                        hpRightDotList.append(Dot(vorLineList[i].bx1,vorLineList[i].by1,math.inf))
                        #print('right b1,dot\n')
                    if ( IsExist(hpRightDotList,vorLineList[i].bx2,vorLineList[i].by2) == 0 ):
                        hpRightDotList.append(Dot(vorLineList[i].bx2,vorLineList[i].by2,math.inf))
                        #print('right b2,dot\n')
            i = i+1
        hpLineList.sort(key = lambda l:(l.interY))
        hpLeftDotList.sort(key = lambda l:(l.y))
        hpRightDotList.sort(key = lambda l:(l.y))

        beforeLenVor = len(vorLineList)
        
        if (count != 0): #沒有交點的還沒處理
            lLen = len(hpLeftDotList)
            rLen = len(hpRightDotList)
            if ( hpLeftDotList[0].y <= hpRightDotList[0].y ):
                if ( lLen == 2 and rLen == 2 ):
                    xdir = 'left'
                    DrawLine(hpLeftDotList[0].x,hpLeftDotList[0].y,hpRightDotList[0].x,hpRightDotList[0].y)
                    xdir = 'right'
                    DrawLine(hpRightDotList[0].x,hpRightDotList[0].y,hpLeftDotList[1].x,hpLeftDotList[1].y)
                    xdir = 'left'
                    DrawLine(hpLeftDotList[1].x,hpLeftDotList[1].y,hpRightDotList[1].x,hpRightDotList[1].y)
                elif ( lLen == 2 and rLen == 3):
                    xdir = 'left'
                    DrawLine(hpLeftDotList[0].x,hpLeftDotList[0].y,hpRightDotList[0].x,hpRightDotList[0].y)
                    xdir = 'right'
                    DrawLine(hpRightDotList[0].x,hpRightDotList[0].y,hpLeftDotList[1].x,hpLeftDotList[1].y)
                    xdir = 'left'
                    DrawLine(hpLeftDotList[1].x,hpLeftDotList[1].y,hpRightDotList[1].x,hpRightDotList[1].y)
                    xdir = 'left'
                    DrawLine(hpLeftDotList[1].x,hpLeftDotList[1].y,hpRightDotList[2].x,hpRightDotList[2].y)
                elif ( lLen == 3 and rLen == 2):
                    xdir = 'left'
                    DrawLine(hpLeftDotList[0].x,hpLeftDotList[0].y,hpRightDotList[0].x,hpRightDotList[0].y)
                    xdir = 'right'
                    DrawLine(hpRightDotList[0].x,hpRightDotList[0].y,hpLeftDotList[1].x,hpLeftDotList[1].y)
                    xdir = 'left'
                    DrawLine(hpLeftDotList[1].x,hpLeftDotList[1].y,hpRightDotList[1].x,hpRightDotList[1].y)
                    xdir = 'right'
                    DrawLine(hpRightDotList[1].x,hpRightDotList[1].y,hpLeftDotList[2].x,hpLeftDotList[2].y)
                else: #3,3
                    xdir = 'left'
                    DrawLine(hpLeftDotList[0].x,hpLeftDotList[0].y,hpRightDotList[0].x,hpRightDotList[0].y)
                    xdir = 'right'
                    DrawLine(hpRightDotList[0].x,hpRightDotList[0].y,hpLeftDotList[1].x,hpLeftDotList[1].y)
                    xdir = 'left'
                    DrawLine(hpLeftDotList[1].x,hpLeftDotList[1].y,hpRightDotList[1].x,hpRightDotList[1].y)
                    xdir = 'right'
                    DrawLine(hpRightDotList[1].x,hpRightDotList[1].y,hpLeftDotList[2].x,hpLeftDotList[2].y)
                    xdir = 'left'
                    DrawLine(hpLeftDotList[2].x,hpLeftDotList[2].y,hpRightDotList[2].x,hpRightDotList[2].y)
                #print('hpL\n')
            else:
                if ( lLen == 2 and rLen == 2 ):
                    xdir = 'right'
                    DrawLine(hpRightDotList[0].x,hpRightDotList[0].y,hpLeftDotList[0].x,hpLeftDotList[0].y)
                    xdir = 'left'
                    DrawLine(hpLeftDotList[0].x,hpLeftDotList[0].y,hpRightDotList[1].x,hpRightDotList[1].y)
                    xdir = 'right'
                    DrawLine(hpRightDotList[1].x,hpRightDotList[1].y,hpLeftDotList[1].x,hpLeftDotList[1].y)
                elif ( lLen == 2 and rLen == 3):
                    xdir = 'right'
                    DrawLine(hpRightDotList[0].x,hpRightDotList[0].y,hpLeftDotList[0].x,hpLeftDotList[0].y)
                    xdir = 'left'
                    DrawLine(hpLeftDotList[0].x,hpLeftDotList[0].y,hpRightDotList[1].x,hpRightDotList[1].y)
                    xdir = 'right'
                    DrawLine(hpRightDotList[1].x,hpRightDotList[1].y,hpLeftDotList[1].x,hpLeftDotList[1].y)
                    xdir = 'left'
                    DrawLine(hpLeftDotList[1].x,hpLeftDotList[1].y,hpRightDotList[2].x,hpRightDotList[2].y)
                elif ( lLen == 3 and rLen == 2):
                    xdir = 'right'
                    DrawLine(hpRightDotList[0].x,hpRightDotList[0].y,hpLeftDotList[0].x,hpLeftDotList[0].y)
                    xdir = 'left'
                    DrawLine(hpLeftDotList[0].x,hpLeftDotList[0].y,hpRightDotList[1].x,hpRightDotList[1].y)
                    xdir = 'right'
                    DrawLine(hpRightDotList[1].x,hpRightDotList[1].y,hpLeftDotList[1].x,hpLeftDotList[1].y)
                    xdir = 'right'
                    DrawLine(hpRightDotList[1].x,hpRightDotList[1].y,hpLeftDotList[2].x,hpLeftDotList[2].y)
                else: #3,3
                    xdir = 'right'
                    DrawLine(hpRightDotList[0].x,hpRightDotList[0].y,hpLeftDotList[0].x,hpLeftDotList[0].y)
                    xdir = 'left'
                    DrawLine(hpLeftDotList[0].x,hpLeftDotList[0].y,hpRightDotList[1].x,hpRightDotList[1].y)
                    xdir = 'right'
                    DrawLine(hpRightDotList[1].x,hpRightDotList[1].y,hpLeftDotList[1].x,hpLeftDotList[1].y)
                    xdir = 'left'
                    DrawLine(hpLeftDotList[1].x,hpLeftDotList[1].y,hpRightDotList[2].x,hpRightDotList[2].y)
                    xdir = 'right'
                    DrawLine(hpRightDotList[2].x,hpRightDotList[2].y,hpLeftDotList[2].x,hpLeftDotList[2].y)
                #print('hpR\n')
                
        i = beforeLenVor+1
        afterLenVor = len(vorLineList)
        #while ( i < afterLenVor-1 ):
            #vorLineList[i].isRay = 'f'
            #i = i+1

        xdir = 'center'    
        i = 0
        j = beforeLenVor
        x1,y1 = 0,0
        x2,y2 = 0,0
        while ( i < len(hpLineList) ):
            if ( j < afterLenVor-1 ):
                if ( j != beforeLenVor ):
                    x1,y1 = FindInter(hpLineList[i-1].x1,hpLineList[i-1].y1,hpLineList[i-1].x2,hpLineList[i-1].y2,vorLineList[j-1].x1,vorLineList[j-1].y1,vorLineList[j-1].x2,vorLineList[j-1].y2)
                    #c.create_oval(x1,y1,x1,y1, width=3, outline=Color())
                x2,y2 = FindInter(hpLineList[i].x1,hpLineList[i].y1,hpLineList[i].x2,hpLineList[i].y2,vorLineList[j].x1,vorLineList[j].y1,vorLineList[j].x2,vorLineList[j].y2)
                c.create_oval(x2,y2,x2,y2, width=3, outline=Color())

                #print('1:'+str(x1)+','+str(y1)+'\n')
                #print('2:'+str(x2)+','+str(y2)+'\n')

                if ( j != beforeLenVor ):
                    c.coords(vorLineList[j].name,x1,y1,x2,y2)
                    vorLineList[j].isRay = 'f'
                    vorLineList[j].x1,vorLineList[j].y1,vorLineList[j].x2,vorLineList[j].y2 = x1,y1,x2,y2
                else:
                    if ( vorLineList[j].y1 > vorLineList[j].y2 ):
                        c.coords(vorLineList[j].name,x2,y2,vorLineList[j].x2,vorLineList[j].y2)
                        vorLineList[j].x1,vorLineList[j].y1,vorLineList[j].x2,vorLineList[j].y2 = x2,y2,vorLineList[j].x2,vorLineList[j].y2
                    else:
                        c.coords(vorLineList[j].name,vorLineList[j].x1,vorLineList[j].y1,x2,y2)
                        vorLineList[j].x1,vorLineList[j].y1,vorLineList[j].x2,vorLineList[j].y2 = vorLineList[j].x1,vorLineList[j].y1,x2,y2
                
                if ( vorLineList[j+1].y1 > vorLineList[j+1].y2 ):
                    c.coords(vorLineList[j+1].name,vorLineList[j+1].x1,vorLineList[j+1].y1,x2,y2)
                    vorLineList[j+1].x1,vorLineList[j+1].y1,vorLineList[j+1].x2,vorLineList[j+1].y2 = vorLineList[j+1].x1,vorLineList[j+1].y1,x2,y2
                else:
                    c.coords(vorLineList[j+1].name,x2,y2,vorLineList[j+1].x2,vorLineList[j+1].y2)
                    vorLineList[j+1].x1,vorLineList[j+1].y1,vorLineList[j+1].x2,vorLineList[j+1].y2 = x2,y2,vorLineList[j+1].x2,vorLineList[j+1].y2

                j = j+1

            if ( hpLineList[i].where == 'left' ):
                if ( hpLineList[i].x1 > hpLineList[i].x2 ):
                    c.coords(hpLineList[i].name,x2,y2,hpLineList[i].x2,hpLineList[i].y2)
                    if ( hpLineList[i].x2 > 0 ):
                        hpLineList[i].isRay = 'f'
                else:
                    c.coords(hpLineList[i].name,hpLineList[i].x1,hpLineList[i].y1,x2,y2)
                    if ( hpLineList[i].x1 > 0 ):
                        hpLineList[i].isRay = 'f'
            else:
                if ( hpLineList[i].x1 < hpLineList[i].x2 ):
                    c.coords(hpLineList[i].name,x2,y2,hpLineList[i].x2,hpLineList[i].y2)
                    if ( hpLineList[i].x2 < 600 ):
                        hpLineList[i].isRay = 'f'
                else:
                    c.coords(hpLineList[i].name,hpLineList[i].x1,hpLineList[i].y1,x2,y2)
                    if ( hpLineList[i].x1 < 600 ):
                        hpLineList[i].isRay = 'f'
            i = i+1
        i = 0
        j = 0
        while ( i < len(hpLineList) ):
            while ( j < len(vorLineList) ):
                if ( hpLineList[i].name == vorLineList[j].name ):
                    vorLineList[j].isRay = hpLineList[i].isRay
                    break
                j = j+1
            i = i+1
            
        c.delete(xbound_id)
        #print(str(count)+'\n')
        print('step5\n')
    else: # step == 6 , 合併convex hull
        
        xdir = 'center'
        i = 0
        while ( i < len(conLineList) ):
            c.delete(conLineList[i].name)
            i = i+1
        conLineList.clear()
        i = 0
        while ( i < len(vorLineList) ):
            if ( vorLineList[i].isRay == 't' ):
                tmpList = [Dot(vorLineList[i].bx1,vorLineList[i].by1,math.inf),
                           Dot(vorLineList[i].bx2,vorLineList[i].by1,math.inf)] #'name'
                tmpList.sort(key = lambda l:(l.x,l.y))
                name = c.create_line(vorLineList[i].bx1,vorLineList[i].by1,vorLineList[i].bx2,vorLineList[i].by2,
                                     width=3, fill=Color())
                # m = (vorLineList[i].by1-vorLineList[i].by2)/(vorLineList[i].bx1-vorLineList[i].bx2) 應該不用紀錄
                
                conLineList.append(Line(tmpList[0].x,tmpList[0].y,tmpList[1].x,tmpList[1].y,
                                        tmpList[0].x,tmpList[0].y,tmpList[1].x,tmpList[1].y, name, 'f', xdir))
            i = i+1
        print('step6\n')
    

def StepByStep(event):
    print('Step By Step\n')
    RunAStep()
    global step
    step = step+1          

#寫檔
def Output(event):
    dotList.sort(key = lambda l:(l.x,l.y))
    vorLineList.sort(key = lambda l:(l.x1,l.y1,l.x2,l.y2))
    fOut = open('voronoi_output.txt', 'w')
    for i in dotList:
        fOut.write('P '+ str(int(i.x)) + ' ' + str(int(i.y)) + '\n')
    for i in vorLineList:
        fOut.write('E '+ str(int(i.x1)) + ' ' + str(int(i.y1)) + ' ' + str(int(i.x2)) + ' ' + str(int(i.y2)) + '\n')


#主視窗
window = Tk()
window.title("Voronoi") 
window.geometry('800x700+800+100')
window.resizable(0,0) #禁止調整視窗大小

#分成左右兩區
fLeft = Frame(window)
fLeft.grid(row=0, column=0)

fRight = LabelFrame(window, borderwidth=3, relief='ridge', text='Input Dot')
fRight.grid(row=0, column=1)

#左上畫布
f1 = Frame(fLeft, borderwidth=3, relief='ridge')
f1.pack()

c = Canvas(f1, width=600, height=600)
c.pack()
c.bind('<Button-1>', MouseDraw)

#右方輸出區
scrollbar = Scrollbar(fRight, orient=VERTICAL)
listbox = Listbox(fRight, yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)
scrollbar.pack(side=RIGHT, fill=Y)
listbox.pack(side=LEFT, fill=BOTH, expand=1)

#左下1
f2 = Frame(fLeft)
f2.pack(pady=10)

label = Label(f2, text='Input File Name')
label.grid(row=0,column=0)

entry = Entry(f2)
entry.grid(row=0,column=1)

bReadFile = Button(f2, text='Read File')
bReadFile.grid(row=0,column=2)
bReadFile.bind('<Button-1>', ReadFile)

#左下2
f3 = Frame(fLeft)
f3.pack(pady=10)

bReadData = Button(f3, text='Read Next Data')
bReadData.grid(row=0,column=0)
bReadData.bind('<Button-1>', ReadData)

bSbs = Button(f3, text='Step By Step')
bSbs.grid(row=0,column=1)
bSbs.bind('<Button-1>', StepByStep)

bRun = Button(f3, text='Run')
bRun.grid(row=0,column=2)
bRun.bind('<Button-1>', RunButton)

bOut = Button(f3, text='Output')
bOut.grid(row=0,column=3)
bOut.bind('<Button-1>', Output)

bClear = Button(f3, text='Clear')
bClear.grid(row=0,column=4)
bClear.bind('<Button-1>', ClearDraw)

#主程式
dotList = []
leftDotList = [] #左邊的點
rightDotList = [] #右邊的點

vorLineList = [] #voronoi(include HP)
conLineList = [] #convex hull

fIn = None #讀檔用
step = 0 #step by step用

xbound = 0 #divide的中線
xbound_id = None

xdir = 'center' #判斷左邊or右邊的線

beforeLenVor = 0
afterLenVor = 0

window.mainloop()

