#-*- coding:utf-8 -*-

import wx
import wx.py.images as images

class Frame(wx.Frame):
    def __init__(self, title, size=wx.DefaultSize, pos=wx.DefaultPosition):
        super(Frame, self).__init__(None, title=title, size=size, pos=pos)

        # 显示工具栏，状态栏，菜单栏
        panel = wx.Panel(self, -1)
        panel.SetBackgroundColour('#FFF')

        statusBar = self.CreateStatusBar()
        toolBar = self.CreateToolBar()

        # image = wx.Image("t.jpg", wx.BITMAP_TYPE_JPEG)
        # toolBar.AddSimpleTool(-1, image.ConvertToBitmap(), "New", "Show help for New")
        toolBar.AddSimpleTool(-1, images.getPyBitmap(), "New", "Show help for New")
        # 准备显示toolbar
        toolBar.Realize()

        # 创建菜单栏
        menuBar = wx.MenuBar()
        # 创建菜单
        menu1 = wx.Menu()
        menuBar.Append(menu1, "File")

        menu2 = wx.Menu()
        menu2.Append(-1, "Copy", "Copy in status bar")
        menu2.Append(-1, "Cut", "")
        menu2.Append(-1, "Paste", "")
        menu2.AppendSeparator()
        menu2.Append(-1, "Options", "display options")

        menuBar.Append(menu2, "Edit")
        self.SetMenuBar(menuBar)

class App(wx.App):
    def OnPreInit(self):
        self.frame = Frame(title="MyApp", size=(550, 400))
        self.frame.Centre(True)
        self.frame.Show(True)
        return True

if __name__ == '__main__':
    app = App(False)
    app.MainLoop()
