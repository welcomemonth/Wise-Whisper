#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Time: 2024/6/30 20:55
@Author: zhengyu
@File: 消息列表
@Desc: zhengyu 2024/6/30 20:55. + cause
"""

import wx
import wx.lib.scrolledpanel as scrolled

from whisper.schema import Message
from whisper.subpage import MessagePanel


class ConversationFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="消息展示框", size=(800, 600))

        # 创建主面板
        panel = wx.Panel(self)

        # 创建水平BoxSizer，用于在水平布局中管理子控件
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        panel.SetSizer(sizer)

        # 创建左侧面板
        self.left_panel = wx.Panel(panel)

        # 创建右侧对话面板
        self.conversation_panel = wx.Panel(panel)
        self.conversation_panel.SetBackgroundColour(wx.WHITE)  # 设置背景颜色为白色

        # 为左侧面板设置垂直BoxSizer
        left_sizer = wx.BoxSizer(wx.VERTICAL)
        self.left_panel.SetSizer(left_sizer)

        # 为右侧对话面板设置垂直BoxSizer
        right_sizer = wx.BoxSizer(wx.VERTICAL)
        self.conversation_panel.SetSizer(right_sizer)

        # 创建一个可滚动面板用于显示消息
        self.message_panel = scrolled.ScrolledPanel(self.conversation_panel, style=wx.SIMPLE_BORDER)
        self.message_panel.SetupScrolling()  # 设置滚动功能
        self.message_sizer = wx.BoxSizer(wx.VERTICAL)  # 使用垂直BoxSizer管理消息
        self.message_panel.SetSizer(self.message_sizer)

        # 将可滚动面板添加到右侧对话面板的Sizer中
        right_sizer.Add(self.message_panel, proportion=1, flag=wx.EXPAND)

        # 将左侧和右侧面板添加到主Sizer中
        sizer.Add(self.left_panel, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)
        sizer.Add(self.conversation_panel, proportion=3, flag=wx.EXPAND | wx.ALL, border=5)

        msg1 = Message("消息内容1", role="user")
        msg2 = Message("消息内容2", role="user")
        msg3 = Message("**消息内容3**", role="assistant")
        msg4 = Message("""小腿按摩可以帮助改善血液循环，缓解肌肉疲劳，并且在一定程度上帮助塑形，但并不能直接“瘦腿”。减肥和塑形主要是通过合理饮食和适量的运动实现的。
        小腿的形状主要由肌肉大小（特别是腓肠肌）以及腿部脂肪堆积决定。定期进行小腿按摩可能会有助于放松紧绷的小腿肌肉，减轻疲劳，减少水肿，并且在一定程度上帮助提高线条感或改善局部皮肤质感。
        若想达到“瘦腿”的目的：
        1. **合理饮食**：控制总体热量摄入，减少高糖、高油脂食物的摄入，增加蔬果和蛋白质的摄取。确保饮食健康均衡。
        2. **有氧运动**：定期进行有氧运动，如快走、慢跑、骑自行车或游泳等，可以燃烧全身脂肪，间接有助于减轻腿部重量。
        3. **针对性锻炼**：专门针对下肢的训练，如蹲起、提踵（踮脚尖）动作，可以帮助塑形并增强肌肉力量。注意在专业指导下进行，避免受伤。
        小腿按摩是一个辅助手段，如果配合以上的方法使用，可能能更好地促进局部改善和整体健康。当然，在开始任何新的锻炼或减肥计划之前，建议咨询专业人士的意见。"""
        )

        # 添加示例消息
        self.add_message(msg1)
        self.add_message(msg2)
        self.add_message(msg3)
        self.add_message(msg4)

        # 显示窗口
        self.Show()

    def add_message(self, message):
        """
        向对话面板中添加消息

        :param message: 消息内容
        """
        # 创建消息面板
        message_panel = MessagePanel(self.message_panel, message)

        # 将消息面板添加到消息Sizer中
        self.message_sizer.Add(message_panel, flag=wx.EXPAND | wx.ALL, border=5)
        # 添加一条横线
        self.message_sizer.Add(wx.StaticLine(self.message_panel), flag=wx.EXPAND | wx.ALL, border=5)
        # 重新布局消息面板
        self.message_panel.Layout()


if __name__ == "__main__":
    # 创建应用程序对象
    app = wx.App(False)

    # 创建主窗口对象
    frame = ConversationFrame()

    # 进入主事件循环
    app.MainLoop()
