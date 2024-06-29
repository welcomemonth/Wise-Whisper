#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Time: 2024/6/29 15:04
@Author: zhengyu
@File: setting_dialog
@Desc zhengyu 2024/6/29 15:04. + cause
"""
import wx


class SettingsDialog(wx.Dialog):
    def __init__(self, parent):
        super(SettingsDialog, self).__init__(parent, title="Settings", size=(400, 300))

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # 在这里添加设置选项和控件
        label = wx.StaticText(panel, label="Settings content")
        vbox.Add(label, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        # 确认和取消按钮
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        okButton = wx.Button(panel, label='OK')
        closeButton = wx.Button(panel, label='Cancel')
        hbox.Add(okButton)
        hbox.Add(closeButton, flag=wx.LEFT, border=5)
        vbox.Add(hbox, flag=wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, border=10)

        panel.SetSizer(vbox)

        okButton.Bind(wx.EVT_BUTTON, self.on_ok)
        closeButton.Bind(wx.EVT_BUTTON, self.on_cancel)

    def on_ok(self, event):
        # 处理确认按钮事件
        self.EndModal(wx.ID_OK)

    def on_cancel(self, event):
        # 处理取消按钮事件
        self.EndModal(wx.ID_CANCEL)