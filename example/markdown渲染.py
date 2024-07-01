#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Time: 2024/6/30 22:31
@Author: zhengyu
@File: markdown渲染
@Desc zhengyu 2024/6/30 22:31. + cause
"""

import wx
import wx.html2
import wx.richtext as rt
from wx.lib.scrolledpanel import ScrolledPanel
import markdown


class MessagePanel(wx.Panel):
    def __init__(self, parent, content, timestamp):
        super().__init__(parent)

        # 创建头像
        avatar = wx.StaticBitmap(self, bitmap=wx.ArtProvider.GetBitmap(wx.ART_INFORMATION, size=(32, 32)))

        # 渲染Markdown内容
        self.message_text = rt.RichTextCtrl(self, style=wx.TE_READONLY | wx.BORDER_NONE | wx.TE_AUTO_URL)
        # self.message_text.SetMinSize((400, 100))
        self.set_content(content)

        # 创建时间戳
        self.timestamp_text = wx.StaticText(self, label=timestamp)

        # 创建按钮
        copy_button = wx.Button(self, label="复制")
        edit_button = wx.Button(self, label="编辑")
        refresh_button = wx.Button(self, label="刷新")
        pin_button = wx.Button(self, label="固定")

        copy_button.Bind(wx.EVT_BUTTON, self.on_copy)
        edit_button.Bind(wx.EVT_BUTTON, self.on_edit)
        refresh_button.Bind(wx.EVT_BUTTON, self.on_refresh)
        pin_button.Bind(wx.EVT_BUTTON, self.on_pin)

        # 布局
        top_sizer = wx.BoxSizer(wx.HORIZONTAL)
        top_sizer.Add(avatar, flag=wx.ALL, border=5)

        text_sizer = wx.BoxSizer(wx.VERTICAL)
        text_sizer.Add(self.message_text, flag=wx.EXPAND | wx.ALL, border=5)
        text_sizer.Add(self.timestamp_text, flag=wx.ALL, border=5)

        top_sizer.Add(text_sizer, proportion=1, flag=wx.EXPAND)

        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        button_sizer.Add(copy_button, flag=wx.ALL, border=5)
        button_sizer.Add(edit_button, flag=wx.ALL, border=5)
        button_sizer.Add(refresh_button, flag=wx.ALL, border=5)
        button_sizer.Add(pin_button, flag=wx.ALL, border=5)

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(top_sizer, proportion=1, flag=wx.EXPAND)
        main_sizer.Add(button_sizer, flag=wx.ALIGN_LEFT)

        self.SetSizer(main_sizer)

        # 保存消息内容
        self.content = content

    def set_content(self, content):
        # 将Markdown内容转换为HTML
        html_content = markdown.markdown(content)
        self.message_text.Clear()
        self.message_text.BeginSuppressUndo()
        self.message_text.BeginParagraphSpacing(0, 20)
        self.message_text.WriteText(html_content)
        self.message_text.EndParagraphSpacing()
        self.message_text.EndSuppressUndo()

    def on_copy(self, event):
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(wx.TextDataObject(self.content))
            wx.TheClipboard.Close()
            wx.MessageBox("消息已复制", "信息", wx.OK | wx.ICON_INFORMATION)

    def on_edit(self, event):
        dialog = wx.TextEntryDialog(self, "编辑消息", "编辑", self.content)
        if dialog.ShowModal() == wx.ID_OK:
            self.content = dialog.GetValue()
            self.set_content(self.content)
        dialog.Destroy()

    def on_refresh(self, event):
        wx.MessageBox("消息已刷新", "信息", wx.OK | wx.ICON_INFORMATION)

    def on_pin(self, event):
        wx.MessageBox("消息已固定", "信息", wx.OK | wx.ICON_INFORMATION)


class ConversationFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="消息展示框", size=(800, 600))

        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        panel.SetSizer(sizer)

        self.left_panel = wx.Panel(panel)
        self.conversation_panel = wx.Panel(panel)

        self.conversation_panel.SetBackgroundColour(wx.WHITE)

        left_sizer = wx.BoxSizer(wx.VERTICAL)
        self.left_panel.SetSizer(left_sizer)

        right_sizer = wx.BoxSizer(wx.VERTICAL)
        self.conversation_panel.SetSizer(right_sizer)

        self.message_panel = ScrolledPanel(self.conversation_panel)
        self.message_panel.SetupScrolling()
        self.message_sizer = wx.BoxSizer(wx.VERTICAL)
        self.message_panel.SetSizer(self.message_sizer)

        right_sizer.Add(self.message_panel, proportion=1, flag=wx.EXPAND)

        sizer.Add(self.left_panel, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)
        sizer.Add(self.conversation_panel, proportion=3, flag=wx.EXPAND | wx.ALL, border=5)

        # 示例消息
        self.current_conversation = self.get_current_conversation()
        [self.add_message(msg.content, msg.timestamp) for msg in self.current_conversation.messages]

        self.Show()

    def add_message(self, content, timestamp):
        message_panel = MessagePanel(self.message_panel, content, timestamp)
        self.message_sizer.Add(message_panel, flag=wx.EXPAND | wx.ALL, border=5)
        self.message_panel.Layout()

    def get_current_conversation(self):
        class Message:
            def __init__(self, content, timestamp):
                self.content = content
                self.timestamp = timestamp

        class Conversation:
            def __init__(self):
                self.messages = [
                    Message("**消息内容1**", "2024/6/25 20:38:12"),
                    Message("**消息内容1**", "2024/6/25 20:38:12"),
                    Message("**消息内容1**", "2024/6/25 20:38:12"),
                    Message("**消息内容1**", "2024/6/25 20:38:12"),
                    Message("**消息内容1**", "2024/6/25 20:38:12"),
                    Message("""小腿按摩可以帮助改善血液循环，缓解肌肉疲劳，并且在一定程度上帮助塑形，但并不能直接“瘦腿”。减肥和塑形主要是通过合理饮食和适量的运动实现的。

小腿的形状主要由肌肉大小（特别是腓肠肌）以及腿部脂肪堆积决定。定期进行小腿按摩可能会有助于放松紧绷的小腿肌肉，减轻疲劳，减少水肿，并且在一定程度上帮助提高线条感或改善局部皮肤质感。

若想达到“瘦腿”的目的：

1. **合理饮食**：控制总体热量摄入，减少高糖、高油脂食物的摄入，增加蔬果和蛋白质的摄取。确保饮食健康均衡。
2. **有氧运动**：定期进行有氧运动，如快走、慢跑、骑自行车或游泳等，可以燃烧全身脂肪，间接有助于减轻腿部重量。
3. **针对性锻炼**：专门针对下肢的训练，如蹲起、提踵（踮脚尖）动作，可以帮助塑形并增强肌肉力量。注意在专业指导下进行，避免受伤。

小腿按摩是一个辅助手段，如果配合以上的方法使用，可能能更好地促进局部改善和整体健康。当然，在开始任何新的锻炼或减肥计划之前，建议咨询专业人士的意见。""", "2024/6/25 20:38:15")
                ]

        return Conversation()


if __name__ == "__main__":
    app = wx.App(False)
    frame = ConversationFrame()
    app.MainLoop()
