#-*- coding:utf-8 -*-

import wx

class Frame(wx.Frame):
    def __init__(self, title, size, pos=wx.DefaultPosition):
        super(Frame, self).__init__(None, title=title, size=size, pos=pos)

        # 显示图片
        image = wx.Image("t.jpg", wx.BITMAP_TYPE_JPEG)
        self.bmp = wx.StaticBitmap(self, bitmap=image.ConvertToBitmap())

class App(wx.App):
    def OnPreInit(self):
        self.frame = Frame(title="MyApp", size=(550, 400))
        self.frame.Centre(True)
        self.frame.Show(True)
        return True

if __name__ == '__main__':
    app = App(False)
    app.MainLoop()
