#-*- coding:utf-8 -*-

import wx
from wx.py.shell import ShellFrame

class Frame(wx.Frame):
    def __init__(self, title, size, pos=wx.DefaultPosition):
        super(Frame, self).__init__(None, title=title, size=size, pos=pos)

        panel = wx.Panel(self, -1)
        panel.SetBackgroundColour('#FFF')

        menuBar = wx.MenuBar()

        menu = wx.Menu()
        shell = menu.Append(-1, "Shell", "Open python shell")

        menuBar.Append(menu, "Open")
        self.Bind(wx.EVT_MENU, self.onShell, shell)
        self.SetMenuBar(menuBar)

    def onShell(self, event):
        sFrame = ShellFrame(self)
        sFrame.Show()

class App(wx.App):
    def OnPreInit(self):
        self.frame = Frame(title="MyApp", size=(550, 400))
        self.frame.Centre(True)
        self.frame.Show(True)
        return True

if __name__ == '__main__':
    app = App(False)
    app.MainLoop()
