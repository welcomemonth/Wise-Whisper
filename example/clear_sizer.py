#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Time: 2024/7/2 10:00
@Author: zhengyu
@File: clear_sizer
@Desc zhengyu 2024/7/2 10:00. + cause
"""
import wx


class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        super(MyFrame, self).__init__(parent, title=title, size=(300, 200))

        panel = wx.Panel(self)
        box = wx.BoxSizer(wx.VERTICAL)

        # 添加一些控件到BoxSizer中
        self.button1 = wx.Button(panel, label='Button 1')
        box.Add(self.button1, 0, wx.ALL, 5)

        self.button2 = wx.Button(panel, label='Button 2')
        box.Add(self.button2, 0, wx.ALL, 5)

        self.delete_button = wx.Button(panel, label='Delete Other Buttons')
        box.Add(self.delete_button, 0, wx.ALL, 5)

        panel.SetSizer(box)

        # 绑定删除按钮的事件
        self.delete_button.Bind(wx.EVT_BUTTON, self.on_delete_buttons)

        self.Show(True)

    def on_delete_buttons(self, event):
        # 从Sizer中移除并销毁其他按钮
        buttons_to_delete = [self.button1, self.button2]

        for button in buttons_to_delete:
            button.Destroy()

        # 重新布局Sizer
        self.Layout()


app = wx.App(False)
frame = MyFrame(None, "Delete Buttons Example")
app.MainLoop()
