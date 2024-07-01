#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Time: 2024/6/30 20:24
@Author: zhengyu
@File: message_panel
@Desc zhengyu 2024/6/30 20:24. + cause
"""
import wx
import markdown
import wx.html2
from whisper.schema import Message
from whisper.util import set_icon


class MessagePanel(wx.Panel):
    def __init__(self, parent, message: Message):
        super().__init__(parent)

        content = message.content
        timestamp = message.created_at

        if message.role == 'user':
            icon_image = set_icon('user.png', 32, 32)
        elif message.role == 'assistant':
            icon_image = set_icon('robot.png', 32, 32)
        else:
            icon_image = set_icon('system.png', 32, 32)

        avatar = wx.StaticBitmap(self, bitmap=icon_image)

        # Create HTML content display
        self.message_html = wx.html2.WebView.New(self)
        self.md2html(content)

        self.timestamp_text = wx.StaticText(self, label=timestamp)

        copy_button = wx.Button(self, label="复制")
        edit_button = wx.Button(self, label="编辑")
        refresh_button = wx.Button(self, label="刷新")
        pin_button = wx.Button(self, label="固定")

        copy_button.Bind(wx.EVT_BUTTON, self.on_copy)
        edit_button.Bind(wx.EVT_BUTTON, self.on_edit)
        refresh_button.Bind(wx.EVT_BUTTON, self.on_refresh)
        pin_button.Bind(wx.EVT_BUTTON, self.on_pin)

        top_sizer = wx.BoxSizer(wx.HORIZONTAL)
        top_sizer.Add(avatar, flag=wx.ALL, border=5)

        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        button_sizer.Add(copy_button, flag=wx.ALL, border=5)
        button_sizer.Add(edit_button, flag=wx.ALL, border=5)
        button_sizer.Add(refresh_button, flag=wx.ALL, border=5)
        button_sizer.Add(pin_button, flag=wx.ALL, border=5)

        top_sizer.Add(button_sizer, proportion=1, flag=wx.EXPAND | wx.TOP, border=5)

        main_sizer = wx.BoxSizer(wx.VERTICAL)

        main_sizer.Add(top_sizer, proportion=0) # proportion=0不参与分配
        main_sizer.Add(self.message_html, proportion=1, flag=wx.ALIGN_LEFT | wx.LEFT | wx.EXPAND, border=5)
        main_sizer.Add(self.timestamp_text, flag=wx.ALIGN_RIGHT | wx.LEFT, border=5)
        self.SetSizer(main_sizer)
        self.Fit()  # 调整面板大小以适应内容

        self.content = content

    def md2html(self, content):
        html_content = markdown.markdown(content)
        styled_html_content = """
        <html> 
        <head>
            <style>
                .content {{
                    word-wrap: break-word;
                    white-space: pre-wrap;
                    overflow-wrap: break-word;
                    word-break: break-word;
                    max-width: 100%;
                    overflow-x: hidden;
                    overflow-y: hidden;
                    display: block;
                }}
                body {{
                    margin: 0;
                    padding: 0;
                }}
            </style>
        </head>
        <body>
            <div class="content">
                {}
            </div>
        </body>
        </html>
        """.format(html_content)
        self.message_html.SetPage(styled_html_content, "")

    def adjust_height(self):
        # 延迟执行，以便 WebView 完成渲染
        wx.CallLater(100, self._adjust_height)

    def _adjust_height(self):
        # 获取 WebView 内容的高度
        script = "document.body.scrollHeight"
        self.message_html.RunScript(script, self._on_get_height)

    def _on_get_height(self, result):
        height = int(result)
        self.SetMinSize((self.GetSize().GetWidth(), height))
        self.GetParent().Layout()
        self.GetParent().FitInside()

    def on_copy(self, event):
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(wx.TextDataObject(self.content))
            wx.TheClipboard.Close()
            wx.MessageBox("消息已复制", "信息", wx.OK | wx.ICON_INFORMATION)

    def on_edit(self, event):
        dialog = wx.TextEntryDialog(self, "编辑消息", "编辑", self.content)
        if dialog.ShowModal() == wx.ID_OK:
            self.content = dialog.GetValue()
            self.md2html(self.content)
        dialog.Destroy()

    def on_refresh(self, event):
        wx.MessageBox("消息已刷新", "信息", wx.OK | wx.ICON_INFORMATION)

    def on_pin(self, event):
        wx.MessageBox("消息已固定", "信息", wx.OK | wx.ICON_INFORMATION)


