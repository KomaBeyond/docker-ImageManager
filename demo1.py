#-*- coding:utf-8 -*-

import wx

class runDemo(wx.Frame):
    def __init__(self, parent, title):
        super(runDemo, self).__init__(parent, title=title)
        self.SetSize((550, 400))
        self.initUI()
        self.Centre(True)
        self.Show(True)

    def initUI(self):
        panel = wx.Panel(self, -1)
        panel.Bind(wx.EVT_MOTION, self.onMove)

        wx.StaticText(panel, -1, "Pos:", pos=(10, 20))
        self.posCtrl = wx.TextCtrl(panel, -1, "", pos=(40, 20))

    def onMove(self, event):
        pos = event.GetPosition()
        self.posCtrl.SetValue("%s, %s" % (pos.x, pos.y))

if __name__ == '__main__':
    dm = wx.App(False)
    runDemo(None, "Demo1")
    dm.MainLoop()