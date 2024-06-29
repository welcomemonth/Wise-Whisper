#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Time: 2024/6/27 10:44
@Author: zhengyu
@File: 自定义按钮示例
@Desc zhengyu 2024/6/27 10:44. + cause
"""

import wx


class MyCustomButton(wx.Button):
    def __init__(self, parent, label="Custom Button", *args, **kwargs):
        super(MyCustomButton, self).__init__(parent, label=label, *args, **kwargs)

        # 绑定绘制事件
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_ENTER_WINDOW, self.on_enter)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.on_leave)
        self.Bind(wx.EVT_LEFT_DOWN, self.on_click)

        # 初始化按钮状态
        self.hover = False
        self.clicked = False

    def on_paint(self, event):
        # 获取绘图上下文
        dc = wx.PaintDC(self)
        rect = self.GetClientRect()

        # 根据状态设置背景颜色
        if self.clicked:
            background_color = wx.Colour(255, 100, 100)  # 点击状态颜色
        elif self.hover:
            background_color = wx.Colour(200, 200, 200)  # 悬停状态颜色
        else:
            background_color = wx.Colour(240, 240, 240)  # 正常状态颜色

        # 填充背景
        dc.SetBrush(wx.Brush(background_color))
        dc.SetPen(wx.Pen(background_color))
        dc.DrawRectangle(rect)

        # 绘制按钮文本
        dc.SetTextForeground(wx.Colour(0, 0, 0))
        dc.DrawLabel(self.GetLabel(), rect, wx.ALIGN_CENTER)

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
        wx.CallLater(100, self.reset_click)  # 延迟调用，恢复点击状态
        event.Skip()

    def reset_click(self):
        self.clicked = False
        self.Refresh()  # 重新绘制按钮


# 示例应用程序
class MyApp(wx.App):
    def OnInit(self):
        frame = wx.Frame(None, title="Custom Button Example")
        panel = wx.Panel(frame)

        sizer = wx.BoxSizer(wx.VERTICAL)
        custom_button = MyCustomButton(panel, label="Click Me!")
        sizer.Add(custom_button, 0, wx.ALL | wx.CENTER, 20)

        panel.SetSizer(sizer)
        frame.Show()
        return True


if __name__ == "__main__":
    app = MyApp(False)
    app.MainLoop()

