#-*- coding:utf-8 -*-

import wx

class BlockWindow(wx.Panel):
    def __init__(self, parent, ID = -1, label = "", pos = wx.DefaultPosition, size = (100, 25)):
        super(BlockWindow, self).__init__(parent, ID, pos, size, wx.RAISED_BORDER, label)

        self.lable = label
        self.SetBackgroundColour('#FFF')
        self.SetMinSize(size)
        self.Bind(wx.EVT_PAINT, self.onPaint)

    def onPaint(self, event):
        sz = self.GetClientSize()
        dc = wx.PaintDC(self)
        w,h = dc.GetTextExtent(self.lable)
        dc.SetFont(self.GetFont())
        dc.DrawText(self.lable, (sz.width-w)/2, (sz.height-h)/2)

class GridSizerFrame(wx.Frame):
    labels = "one two three four five six seven eight nine".split()

    flags = {
        "one": wx.ALIGN_BOTTOM,
        "two": wx.ALIGN_CENTER,
        "four": wx.ALIGN_RIGHT,
        "six": wx.EXPAND,
        "seven": wx.EXPAND,
        "eight": wx.SHAPED
    }

    def __init__(self):
        super(GridSizerFrame, self).__init__(None, -1, "Sizer Demo")

        sizer = wx.GridSizer(rows = 3, cols = 3, hgap = 5, vgap = 5)

        for label in self.labels:
            bw = BlockWindow(self, label = label, size = (300 ,200))
            flag = self.flags.get(label, 0)
            sizer.Add(bw, 0, flag|wx.ALL, 10)

        self.SetSizer(sizer)
        self.Fit()
        self.SetBackgroundColour('#0000FF')

class GridBagSizerFrame(wx.Frame):
    labels = "one two three four five six seven eight nine".split()

    def __init__(self):
        super(GridBagSizerFrame, self).__init__(None, -1, "Sizer Demo")

        sizer = wx.GridBagSizer(hgap = 5, vgap = 5)

        for col in range(3):
            for row in range(3):
                bw = BlockWindow(self, label=self.labels[row*3+col])
                sizer.Add(bw, pos=(row, col))

        #跨行
        bw = BlockWindow(self, label="span 3 rows")
        sizer.Add(bw, pos=(0, 3), span=(3, 1), flag=wx.EXPAND)

        #跨列
        bw = BlockWindow(self, label="all")
        sizer.Add(bw, pos=(3, 0), span=(1, 4), flag=wx.EXPAND)

        sizer.AddGrowableCol(3)
        sizer.AddGrowableRow(3)

        self.SetSizer(sizer)
        self.Fit()

class App(wx.App):
    def OnPreInit(self):

        self.frame = GridBagSizerFrame()

        self.frame.Centre(True)
        self.frame.Show(True)
        return True

if __name__ == '__main__':
    app = App(False)
    app.MainLoop()
