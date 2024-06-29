#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Time: 2024/6/29 15:14
@Author: zhengyu
@File: setting_panel
@Desc zhengyu 2024/6/29 15:14. + cause
"""
import wx


class SettingsPanel(wx.Panel):
    def __init__(self, parent):
        super(SettingsPanel, self).__init__(parent)

        # 创建设置面板的内容
        self.create_ui()

    def create_ui(self):
        vbox = wx.BoxSizer(wx.VERTICAL)

        label = wx.StaticText(self, label="Settings Panel Content")
        vbox.Add(label, 0, wx.ALIGN_CENTER | wx.ALL, 10)

        # 添加设置选项和控件
        # 这里可以根据需要添加更多设置项

        self.SetSizer(vbox)

