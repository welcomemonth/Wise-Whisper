#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Time: 2024/6/27 10:46
@Author: zhengyu
@File: wx_control自定义按钮
@Desc zhengyu 2024/6/27 10:46. + cause
"""

import wx


class MyCustomButton(wx.Control):
    def __init__(self, parent, label="Custom Button", *args, **kwargs):
        super(MyCustomButton, self).__init__(parent, *args, **kwargs)

        self.label = label

        # 绑定绘制事件
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_ENTER_WINDOW, self.on_enter)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.on_leave)
        self.Bind(wx.EVT_LEFT_DOWN, self.on_click)
        self.Bind(wx.EVT_LEFT_UP, self.on_release)

        # 初始化按钮状态
        self.hover = False
        self.clicked = False

    def on_paint(self, event):
        # 获取绘图上下文
        dc = wx.PaintDC(self)
        rect = self.GetClientRect()

        # 设置背景颜色
        if self.clicked:
            background_color = wx.Colour(255, 100, 100)  # 点击状态颜色
        elif self.hover:
            background_color = wx.Colour(200, 200, 200)  # 悬停状态颜色
        else:
            background_color = wx.Colour(255, 255, 255)  # 正常状态颜色

        # 绘制倒角矩形
        dc.SetBrush(wx.Brush(background_color))
        dc.SetPen(wx.Pen(background_color))
        dc.DrawRoundedRectangle(0, 0, rect.width, rect.height, 10)  # 倒角半径为10

        # 绘制按钮文本
        dc.SetTextForeground(wx.Colour(0, 0, 0))
        dc.DrawLabel(self.label, rect, wx.ALIGN_CENTER)

    def on_enter(self, event):
        self.hover = True
        self.Refresh()  # 重新绘制按钮
        event.Skip()

    def on_leave(self, event):
        self.hover = False
        self.Refresh()  # 重新绘制按钮
        event.Skip()

    def on_click(self, event):
        self.clicked = True
        self.Refresh()  # 重新绘制按钮
        event.Skip()

    def on_release(self, event):
        self.clicked = False
        self.Refresh()  # 重新绘制按钮
        event.Skip()


# 示例应用程序
class MyApp(wx.App):
    def OnInit(self):
        frame = wx.Frame(None, title="Custom Button Example")
        panel = wx.Panel(frame)

        panel.SetBackgroundColour(wx.Colour(100, 149, 237))

        sizer = wx.BoxSizer(wx.VERTICAL)
        custom_button = MyCustomButton(panel, label="Click", size=(50, 50))
        sizer.Add(custom_button, 0, wx.ALL | wx.CENTER, 20)

        panel.SetSizer(sizer)
        frame.Show()
        return True


if __name__ == "__main__":
    app = MyApp(False)
    app.MainLoop()

