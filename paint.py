#-*- coding:utf-8 -*-

import wx
from wx.lib import buttons

class PaintWindow(wx.Window):
    def __init__(self, parent, ID):
        wx.Window.__init__(self, parent, ID)
        self.SetBackgroundColour('#FFF')

        self.color = '#000'
        self.thickness = 1

        # 创建 pen 对象
        self.pen = wx.Pen(self.color, self.thickness, wx.SOLID)

        self.lines = []
        self.curLine = []
        self.pos = (0, 0)

        self.initBuffer()

        self.Bind(wx.EVT_LEFT_DOWN, self.onLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.onLeftUp)
        self.Bind(wx.EVT_MOTION, self.onMotion)
        self.Bind(wx.EVT_SIZE, self.onSize)
        self.Bind(wx.EVT_IDLE, self.onIdle)  # 空闲时事件处理
        self.Bind(wx.EVT_PAINT, self.onPaint)

    def initBuffer(self):
        size = self.GetClientSize()

        # 创建一个缓存的设备上下文, 临时的
        self.buffer = wx.EmptyBitmap(size.width, size.height)
        dc = wx.BufferedDC(None, self.buffer)

        # 使用设备上下文
        dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
        dc.Clear() #产生 EVT_PAINT 事件

        self.drawLines(dc)
        self.reInitBuffer = False

    def getLinesData(self):
        return self.lines[:]

    def setLinesData(self, lines):
        self.lines = lines[:]
        self.initBuffer()
        self.Refresh()

    def drawLines(self, dc):
        for color, thickness, line in self.lines:
            pen = wx.Pen(color, thickness, wx.SOLID)
            dc.SetPen(pen)

            for coords in line:
                dc.DrawLine(*coords)

    def setColor(self, color):
        self.color = color
        self.pen = wx.Pen(self.color, self.thickness, wx.SOLID)

    def setThickness(self, thickness):
        self.thickness = thickness
        self.pen = wx.Pen(self.color, self.thickness, wx.SOLID)

    def onLeftDown(self, event):
        self.curLine = []
        self.pos = event.GetPositionTuple() #获取到鼠标精确位置的坐标元组
        # 在窗口内部捕获鼠标，这样鼠标只响应窗口内的动作，当鼠标移出到窗口外之后动作无效
        # 这必须使用 ReleaseMouse 函数来释放鼠标捕获，否则会出现改窗口没办法通过鼠标关闭
        self.CaptureMouse()

    def onLeftUp(self, event):
        if self.HasCapture():
            self.lines.append((self.color, self.thickness, self.curLine))
            self.curLine = []
            self.ReleaseMouse()

    def onMotion(self, event):
        # 判断鼠标是否在移动中绘制线条
        if event.Dragging() and event.LeftIsDown():
            # 创建另外一个临时缓存并使用 ClientDC 作为主要的上下文设备
            dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)
            self.drawMotion(dc, event)
        event.Skip()

    def drawMotion(self, dc, event):
        dc.SetPen(self.pen)

        newPos = event.GetPositionTuple()

        # 得到旧的点位置（onLeftDown 时的位置）
        # 得到当前点的位置
        # 组合新旧点信息，然后告诉 dc 去绘画
        coords = self.pos+newPos

        self.curLine.append(coords)

        # 绘制一条线条到屏幕上
        dc.DrawLine(*coords)
        self.pos = newPos

    def onSize(self, event):
        self.reInitBuffer = True

    def onIdle(self, event):
        if self.reInitBuffer:
            self.initBuffer()
            self.Refresh(False)

    def onPaint(self, event):
        dc = wx.BufferedPaintDC(self, self.buffer)

class ContorlPanel(wx.Panel):
    BMP_SIZE = 6
    BMP_BORDER = 3
    NUM_COLS = 4
    SPACING = 4

    colorList = (
        '#FF0000', '#00FF00', '#0000FF', '#FFFF00',
        '#FF0011', '#11FF11', '#0550FF', '#CCFF77',
        '#FF0022', '#22FF22', '#0440FF', '#FFAF99',
        '#FF0033', '#33FF33', '#5445FF', '#FFDFAA'
    )

    maxThickness = 16

    def __init__(self, parent, ID, paintWindow):
        wx.Panel.__init__(self, parent, ID, style=wx.RAISED_BORDER)
        self.paintWindow = paintWindow

        buttonSize = (self.BMP_SIZE+2*self.BMP_BORDER, self.BMP_SIZE+2*self.BMP_BORDER)

        colorGrid = self.createColorGrid(parent, buttonSize)
        thicknessGrid = self.createThincknessGrid(buttonSize)

        self.layout(colorGrid, thicknessGrid)

    def createColorGrid(self, parent, buttonSize):
        self.colorMap = {}
        self.colorButtons = {}
        colorGrid = wx.GridSizer(cols = self.NUM_COLS, hgap = 2, vgap = 2)

        # for eachColor in self.colorList:
        #     bmp = parent.MakeBitmap(eachColor)
        #
        #     b = buttons.GenBitmapToggleButton(self, -1, bmp, size = buttonSize)
        #     b.SetBezelWidth(1)
        #     b.SetUseFocusIndicator(False)
        #
        #     self.Bind(wx.EVT_BUTTON, self.onSetColor, b)
        #     colorGrid.Add(b, 0)
        #     self.colorMap[b.GetId()] = eachColor
        #     self.colorButtons[eachColor] = b
        #
        # self.colorButtons[self.colorList[0]].SetToggle(True)

        for eachColor in self.colorList:
            b = wx.Button(self, -1, str(eachColor))
            colorGrid.Add(b)

        return colorGrid

    def createThincknessGrid(self, buttonSize):
        self.thincknessIdMap = {}
        self.thincknessButtons = {}
        thincknessGrid = wx.GridSizer(cols = self.NUM_COLS, hgap = 2, vgap = 2)

        # for x in range(1, self.maxThickness+1):
        #     b = buttons.GenBitmapToggleButton(self, -1, str(x), size = buttonSize)
        #     b.SetBezelWidth(1)
        #     b.SetUseFocusIndicator(False)
        #
        #     self.Bind(wx.EVT_BUTTON, self.onSetThinckness, b)
        #     thincknessGrid.Add(b, 0)
        #
        #     self.thincknessIdMap[b.GetId()] = x
        #     self.thincknessButtons[x] = b
        #
        # self.thincknessButtons[1].SetToggle(True)

        for x in range(1, self.maxThickness + 1):
            b = wx.Button(self, -1, str(x))
            thincknessGrid.Add(b)

        return  thincknessGrid

    def onSetColor(self, event):
        pass

    def onSetThinckness(self, event):
        pass

    def layout(self, colorGrid, thincknessGrid):
        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(colorGrid, 0, wx.ALL, self.SPACING)
        box.Add(thincknessGrid, 0, wx.ALL, self.SPACING)

        self.SetSizer(box)
        box.Fit(self)

class TopPanel(wx.Panel):
    def __init__(self, parent, ID):
        wx.Panel.__init__(self, parent, ID, style=wx.RAISED_BORDER)

        btn = wx.Button(self, -1, "Bttton")


class MainPanel(wx.Frame):
    SPACING = 4

    def __init__(self, parent, ID, paintWindow):
        wx.Frame.__init__(self, parent, ID, style=wx.RAISED_BORDER)

        topPanel = TopPanel(self, -1)

        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(topPanel, 0, wx.ALL)
        box.Add(paintWindow, 1, wx.ALL)
        self.SetSizer(box)
        box.Fit(self)


class Frame(wx.Frame):
    def __init__(self, title, size, pos=wx.DefaultPosition):
        super(Frame, self).__init__(None, title=title, size=size, pos=pos)

        self.paintWindow = PaintWindow(self, -1)

        # 创建状态栏用来显示当前鼠标位置
        self.initStatusBar()

        # 创建菜单栏
        self.createMenuBar()

        # 创建工具栏
        # self.createToolBar()

        # 创建Panel
        self.createPanel()

    def createPanel(self):
        controlPanel = ContorlPanel(self, -1, self.paintWindow)
        mainPanel = MainPanel(self, -1, self.paintWindow)

        box = wx.BoxSizer(wx.HORIZONTAL)
        box.Add(controlPanel, 0, wx.EXPAND)
        box.Add(mainPanel, 1, wx.EXPAND)

        self.SetSizer(box)

    def createToolBar(self):
        pass

    def initStatusBar(self):
        self.paintWindow.Bind(wx.EVT_MOTION, self.showMousePosition)
        self.statusbar = self.CreateStatusBar()
        # 设置状态栏域数量及各域之间的宽度比例
        self.statusbar.SetFieldsCount(3)
        self.statusbar.SetStatusWidths([-2, -2, -2])  # 负数表示占用比例，正数表示绝对宽度

    def showMousePosition(self, event):
        self.statusbar.SetStatusText("Pos: %s" % str(event.GetPositionTuple()), 0)
        self.statusbar.SetStatusText("Current Pts: %s" % len(self.paintWindow.curLine), 1)
        self.statusbar.SetStatusText("Line Count: %s" % len(self.paintWindow.lines), 2)
        event.Skip()

    def createMenuBar(self):
        menuBar = wx.MenuBar()

        for eachMenuData in self.menuData():
            menuLabel = eachMenuData[0]
            menuItems = eachMenuData[1]
            menuBar.Append(self.createMenu(menuItems), menuLabel)

        self.SetMenuBar(menuBar)

    def createMenu(self, menuItems):
        menu = wx.Menu()

        for eachItem in menuItems:
            if len(eachItem) == 2:
                label = eachItem[0]
                subMenu = self.createMenu(eachItem[1])
                menu.AppendMenu(-1, label, subMenu)
            else:
                self.createMenuItem(menu, *eachItem)

        return menu

    def createMenuItem(self, menu, label, status, handler, kind = wx.ITEM_NORMAL):
        if not label:
            menu.AppendSeparator()
            return

        menuItem = menu.Append(-1, label, status, kind)
        self.Bind(wx.EVT_MENU, handler, menuItem)

    def menuData(self):
        return [
            ("File", (
                ("New", "New file", self.onNew),
                ("Open", "Open file", self.onOpen),
                ("Save", "Save file", self.onSave),
                ("", "", ""),
                ("Color", (
                    ("Black", "", self.onColor, wx.ITEM_RADIO),
                    ("Red", "", self.onColor, wx.ITEM_RADIO),
                    ("Green", "", self.onColor, wx.ITEM_RADIO),
                    ("Other", "", self.onOtherColor, wx.ITEM_RADIO),
                    ("", "", "")
                )),
                ("Quit", "Quit", self.onCloseWindow)
            ))
        ]

    def onNew(self, event): pass
    def onOpen(self, event): pass
    def onSave(self, event): pass

    def onOtherColor(self, event):
        dlg = wx.ColourDialog(self)
        dlg.GetColourData().SetChooseFull(True)

        if dlg.ShowModal() == wx.ID_OK:
            self.paintWindow.setColor(dlg.GetColourData().GetColour())

        dlg.Destroy()

    def onColor(self, event):
        menuBar = self.GetMenuBar()
        itemId = event.GetId()
        item = menuBar.FindItemById(itemId)
        color = item.GetLabel()
        self.paintWindow.setColor(color)

    def onCloseWindow(self, event):
        self.Destroy()

    # def MakeBitmap(self, color):
    #     bmp = wx.EmptyBitmap(16, 15)
    #     dc = wx.MemoryDC(bmp)
    #     dc.SetBackground(wx.Brush(color))
    #     dc.Clear()
    #     dc.SelectObject(wx.NullBitmap)
    #     return bmp

class App(wx.App):
    def OnPreInit(self):
        self.frame = Frame(title="Paint", size=(550, 400))
        self.frame.Centre(True)
        self.frame.Show(True)
        return True

if __name__ == '__main__':
    app = App(False)
    app.MainLoop()
