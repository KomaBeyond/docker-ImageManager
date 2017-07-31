#-*- coding:utf-8 -*-

''''
Docker image manager

@author koma <komazhang@foxmail.com>
'''

import wx
import subprocess

class CommanderPanel(wx.Panel):
    def __init__(self, parent, mainFrame, ID = -1, label = "", pos = wx.DefaultPosition, size = wx.DefaultSize):
        super(CommanderPanel, self).__init__(parent, ID, pos, size, wx.RAISED_BORDER, label)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetBackgroundColour('#FFF')
        self.SetMinSize(size)
        self.SetSizer(self.sizer)

    def createNewImageItem(self):
        imgItem = wx.Button(self, -1, "Image-1")

        self.sizer.Add(imgItem, 0, flag=wx.EXPAND)
        self.Fit()

        return  imgItem

class StagePanel(wx.Panel):
    def __init__(self, parent, mainFrame, ID = -1, label = "", pos = wx.DefaultPosition, size = wx.DefaultSize):
        super(StagePanel, self).__init__(parent, ID, pos, size, wx.RAISED_BORDER, label)

        self.SetBackgroundColour('#FFF')
        self.SetMinSize(size)
        self.layout()

    def layout(self):
        sizer = wx.BoxSizer(wx.VERTICAL)

        propsPanel = PropsPanel(self, label="propsPanel", size=(0, 180))
        studioPanel = StudioPanel(self, label="studioPanel")

        sizer.Add(propsPanel, 0, flag=wx.EXPAND)
        sizer.Add(studioPanel, 1, flag=wx.EXPAND)

        self.SetSizer(sizer)
        self.Fit()

    def getBgColor(self):
        return '#FFF'

class PropsPanel(wx.Panel):
    def __init__(self, parent, ID = -1, label = "", pos = wx.DefaultPosition, size = wx.DefaultSize):
        super(PropsPanel, self).__init__(parent, ID, pos, size, wx.RAISED_BORDER, label)

        self.SetBackgroundColour(parent.getBgColor())
        self.SetMinSize(size)

class StudioPanel(wx.Panel):
    def __init__(self, parent, ID = -1, label = "", pos = wx.DefaultPosition, size = wx.DefaultSize):
        super(StudioPanel, self).__init__(parent, ID, pos, size, wx.RAISED_BORDER, label)

        self.SetBackgroundColour(parent.getBgColor())
        self.SetMinSize(size)

class Utils(object):
    @staticmethod
    def execShellCommand(cmd):
        try:
            proc = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdOut, stdErr = proc.communicate()
            return stdOut, stdErr
        except ValueError, err:
            return None, err.message

class MainFrame(wx.Frame):
    def __init__(self, title, size):
        super(MainFrame, self).__init__(None, title=title, size=size)

        self.images = self.initImages()

        self.SetMinSize(size)
        self.SetBackgroundColour('#FFF')
        self.statusBar = self.createStatusBar()
        self.menuBar = self.createMenuBar()
        self.layout()

    def initImages(self):
        stdOut, stdErr = Utils.execShellCommand("docker images")
        print stdOut.split("\n")

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
            ("Image", (
                ("New", "New image", self.onNew),
                ("", "", ""),
                ("Build", "Build image ", self.onBuild),
                ("", "", ""),
                ("Quit", "Quit", self.onCloseWindow)
            ))
        ]

    def onNew(self, event):
        self.commanderPanel.createNewImageItem()

    def onBuild(self, event):
        pass

    def onCloseWindow(self, event):
        self.Destroy()

    def createStatusBar(self):
        statusBar = self.CreateStatusBar()
        return statusBar

    def layout(self):
        splitter = wx.SplitterWindow(self)

        self.commanderPanel = CommanderPanel(splitter, self, label="commanderPanel", size=(180, 0))
        self.stagePanel = StagePanel(splitter, self, label="stagePanel")

        splitter.SplitVertically(self.commanderPanel, self.stagePanel, 180)

class App(wx.App):
    def OnPreInit(self):
        self.frame = MainFrame(title="Docker-ImageManager", size=(950, 600))
        self.frame.Centre(True)
        self.frame.Show(True)
        return True

if __name__ == '__main__':
    app = App(False)
    app.MainLoop()
