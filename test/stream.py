#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Time: 2024/6/25 13:28
@Author: zhengyu
@File: stream
@Desc zhengyu 2024/6/25 13:28. + cause
"""
import wx
import threading
from openai import OpenAI
from whisper.llm_provider.llm_openai import llm


# 假设 OpenAI API 的使用方式和返回结果
class OpenAI:
    @staticmethod
    def ask(messages, model='llama2:13b'):
        return llm.chat.completions.create(
            model=model,
            messages=messages,
            stream=True
        )


class MyFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(MyFrame, self).__init__(*args, **kwargs)

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        self.output_text_ctrl = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY)
        vbox.Add(self.output_text_ctrl, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)

        btn = wx.Button(panel, label='Start Stream')
        vbox.Add(btn, flag=wx.EXPAND | wx.ALL, border=10)

        panel.SetSizer(vbox)

        btn.Bind(wx.EVT_BUTTON, self.on_start_stream)

        self.Show()

    def on_start_stream(self, event):
        thread = threading.Thread(target=self.stream_output)
        thread.start()

    def stream_output(self):
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Who won the world series in 2020?"},
            {"role": "assistant", "content": "The LA Dodgers won in 2020."},
            {"role": "user", "content": "给我讲一个冷笑话"}
        ]

        # 模拟 OpenAI 的 ask 方法返回结果的流式输出
        for chunk in OpenAI.ask(messages):
            # 获取流式输出的响应内容
            response_content = chunk.choices[0].delta.content

            # 在主线程中更新 wx.TextCtrl 的内容
            wx.CallAfter(self.update_output, response_content)

            # 模拟处理每个 chunk 的时间（可以根据实际情况调整）
            # time.sleep(0.5)

    def update_output(self, text):
        current_text = self.output_text_ctrl.GetValue()
        new_text = current_text + text

        # 更新 wx.TextCtrl 的内容
        self.output_text_ctrl.SetValue(new_text)


if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame(None, title='Streaming Output Example', size=(600, 400))
    app.MainLoop()
