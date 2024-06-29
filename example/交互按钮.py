#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Time: 2024/6/29 15:58
@Author: zhengyu
@File: 交互按钮
@Desc zhengyu 2024/6/29 15:58. + cause
"""
# !/usr/bin/python
# -*- coding: utf-8 -*-

'''
translated by achen @2017/10
===
ZetCode wxPython tutorial

This example shows an interactive button.

author: Jan Bodnar
website: www.zetcode.com
last modified: September 2011
'''

import wx
from wx.lib.buttons import GenButton


class Example(wx.Frame):

    def __init__(self, *args, **kwargs):
        super(Example, self).__init__(*args, **kwargs)

        self.InitUI()

    def InitUI(self):
        panel = wx.Panel(self)

        btn = GenButton(panel, label='Button',
                        pos=(100, 100))
        btn.SetBezelWidth(2)
        btn.SetBackgroundColour('DARKGREY')

        btn.Bind(wx.EVT_ENTER_WINDOW, self.OnEnter)
        btn.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeave)


        self.SetSize((300, 200))
        self.SetTitle('Interactive button')
        self.Centre()
        self.Show(True)

    def OnEnter(self, e):
        btn = e.GetEventObject()
        print("enter")
        btn.SetBackgroundColour((255, 0, 0))
        btn.Refresh()

    def OnLeave(self, e):
        btn = e.GetEventObject()
        print("leave")
        btn.SetBackgroundColour((0, 255, 0))
        btn.Refresh()


def main():
    ex = wx.App()
    Example(None)
    ex.MainLoop()


if __name__ == '__main__':
    main()