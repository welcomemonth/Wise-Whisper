'''
   Copyright 2023 Ben Z. Yuan (chatgpt-client@bzy-xyz.com)

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
'''

import wx
import wx.lib.scrolledpanel as scrolled
from typing import Optional
import threading
import sys
import json
import webbrowser
from logger import logger
from whisper.util import set_icon
from whisper.subpage import SettingsDialog, MessagePanel
from whisper.schema.schema import Message, Conversation, load_conversations, save_conversations
from whisper.llm_provider.ollama_api import OllamaLLM

llm = OllamaLLM()

# todo 数据存储到当前目录下
# todo UI设计在right_text中应该有多个消息框，这样不用刷新整个right_text
# todo 自定义按钮
# todo 7/1号 将消息列表重构
# todo 7/2号 重构UI之后，AI问答无法使用
ID_TIMER = 1


class ChatClient(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(ChatClient, self).__init__(*args, **kwargs)

        # 初始化实例属性
        self.conversations: list[Conversation] = []
        self.current_conversation: Optional[Conversation] = None
        self.current_conversation_idx: int = 0
        self.left_panel = None
        self.left_list = None
        self.new_conversation_button = None
        self.conversation_panel = None
        self.right_panel = None
        self.input_text = None
        self.send_button = None

        self.timer = wx.Timer(self, ID_TIMER)
        self.blick = 0

        self.init_ui()
        self.load_message()
        self.on_load_data()

        self.Bind(wx.EVT_CLOSE, self.on_close)
        self.SetSize((900, 600))
        self.Center()
        self.Show()

    def init_ui(self):
        self.create_left_panel()
        self.create_right_panel()

        self.statusbar = self.CreateStatusBar()  #
        self.statusbar.SetStatusText('Welcome to Isabelle')
        # 事件到时之后的操作绑定
        self.Bind(wx.EVT_TIMER, self.on_timer, id=ID_TIMER)

        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        main_sizer.Add(self.left_panel, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)
        main_sizer.Add(self.right_panel, proportion=3, flag=wx.EXPAND | wx.ALL, border=10)

        self.SetSizer(main_sizer)

    def create_left_panel(self):

        self.left_panel = wx.Panel(self)
        left_sizer = wx.BoxSizer(wx.VERTICAL)

        # 创建一个块，包含小标题和两个水平按钮
        block_sizer = wx.BoxSizer(wx.VERTICAL)
        # 小标题
        inner_title = wx.StaticText(self.left_panel, label="Block Title", style=wx.ALIGN_CENTER)
        inner_title.SetFont(wx.Font(wx.FontInfo(16).Bold()))
        inner_title.SetForegroundColour(wx.Colour(0, 0, 0))
        block_sizer.Add(inner_title, flag=wx.EXPAND | wx.ALL, border=10)

        # 水平按钮容器
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)

        button1 = wx.Button(self.left_panel, label="Button 1")
        button2 = wx.Button(self.left_panel, label="Button 2")
        button_sizer.Add(button1, flag=wx.EXPAND | wx.ALL, border=10)
        button_sizer.Add(button2, flag=wx.EXPAND | wx.ALL, border=10)
        block_sizer.Add(button_sizer, flag=wx.EXPAND | wx.ALL)

        self.left_list = wx.ListBox(self.left_panel, style=wx.LB_SINGLE | wx.LB_ALWAYS_SB)
        self.left_list.Bind(wx.EVT_LISTBOX, self.on_conversation_list_selected)

        self.bottom_button_sizer = wx.BoxSizer(wx.HORIZONTAL)

        setting_button = wx.Button(self.left_panel)
        setting_button.SetBitmap(set_icon("icon/cog.png"))
        setting_button.Bind(wx.EVT_BUTTON, self.on_settings_button_click)
        # setting_button.SetMinSize((40, 40))

        github_button = wx.Button(self.left_panel)
        github_button.SetBitmap(set_icon("icon/github.png"))
        # 给按钮绑定点击事件
        github_button.Bind(wx.EVT_BUTTON, self.on_github_button_click)

        self.new_conversation_button = wx.Button(self.left_panel, label="New")
        self.new_conversation_button.SetBitmap(set_icon("../assets/icon/plus.png"))
        self.new_conversation_button.Bind(wx.EVT_BUTTON, self.on_new_conversation)
        self.bottom_button_sizer.Add(setting_button, flag=wx.EXPAND | wx.ALL, border=10)
        self.bottom_button_sizer.Add(github_button, flag=wx.EXPAND | wx.ALL, border=10)
        self.bottom_button_sizer.Add(self.new_conversation_button, flag=wx.EXPAND | wx.ALL, border=10)

        left_sizer.Add(block_sizer, flag=wx.EXPAND | wx.ALL, border=10)
        left_sizer.Add(self.left_list, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)
        left_sizer.Add(self.bottom_button_sizer, flag=wx.EXPAND | wx.ALL, border=10)

        self.left_panel.SetSizer(left_sizer)

    def create_right_panel(self):
        self.right_panel = wx.Panel(self)
        right_sizer = wx.BoxSizer(wx.VERTICAL)

        font = wx.Font(wx.FontInfo(12))
        if not font.SetFaceName("Courier New"):
            font.SetFamily(wx.FONTFAMILY_TELETYPE)

        # 创建一个可滚动面板用于显示消息
        self.conversation_panel = scrolled.ScrolledPanel(self.right_panel, style=wx.SIMPLE_BORDER)
        self.conversation_panel.SetupScrolling()  # 设置滚动功能
        self.conversation_sizer = wx.BoxSizer(wx.VERTICAL)  # 使用垂直BoxSizer管理消息
        self.conversation_panel.SetSizer(self.conversation_sizer)

        self.button_sizer = wx.BoxSizer(wx.HORIZONTAL)  # 在输入栏上方有一排按钮
        self.model_list_cb = wx.ComboBox(self.right_panel, style=wx.CB_DROPDOWN)  # 一个模型选择框

        self.button_sizer.Add(wx.Button(self.right_panel, label="Copy"), flag=wx.ALL, border=10)
        self.button_sizer.Add(self.model_list_cb, 1, flag=wx.ALL | wx.EXPAND, border=10)  # 1代表可扩展，即随着窗口变大而变大
        self.clear_button = wx.Button(self.right_panel, label="Clear")
        self.clear_button.Bind(wx.EVT_BUTTON, self.on_clear)
        self.button_sizer.Add(self.clear_button, flag=wx.ALL, border=10)
        self.button_sizer.Add(wx.Button(self.right_panel, label="Find"), flag=wx.ALL, border=10)
        self.button_sizer.Add(wx.Button(self.right_panel, label="Settings"), flag=wx.ALL, border=10)

        # Create a vertical sizer for the input text and send button
        input_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.input_text = wx.TextCtrl(self.right_panel, size=(-1, 60), style=wx.TE_MULTILINE | wx.TE_PROCESS_ENTER)
        self.input_text.Bind(wx.EVT_TEXT_ENTER, self.on_enter_pressed)
        self.input_text.SetFont(font)

        self.send_button = wx.Button(self.right_panel, label="Send")
        self.send_button.Bind(wx.EVT_BUTTON, self.on_send_pressed)
        input_sizer.Add(self.input_text, 1, wx.EXPAND | wx.RIGHT | wx.LEFT | wx.BOTTOM, border=10)
        input_sizer.Add(self.send_button, 0, wx.EXPAND | wx.RIGHT | wx.LEFT | wx.BOTTOM, border=10)

        right_sizer.Add(self.conversation_panel, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)
        right_sizer.Add(wx.StaticLine(self.right_panel), flag=wx.EXPAND | wx.RIGHT | wx.LEFT, border=10)
        right_sizer.Add(self.button_sizer, flag=wx.EXPAND)
        right_sizer.Add(input_sizer, flag=wx.EXPAND | wx.RIGHT | wx.BOTTOM, border=10)
        self.right_panel.SetSizer(right_sizer)

    def add_message_panel(self, message: Message):
        """
        向对话面板和当前对话框的messages列表中添加消息

        :param message: 消息内容

        """
        # 创建消息面板
        message_panel = MessagePanel(self.conversation_panel, message)
        message_panel.SetMinSize((-1, 400))  # 这个地方应该时动态显示
        # 将消息面板添加到消息Sizer中
        self.conversation_sizer.Add(message_panel, flag=wx.EXPAND | wx.ALL, border=5)
        self.conversation_sizer.Add(wx.StaticLine(self.conversation_panel), flag=wx.EXPAND | wx.ALL, border=5)
        # 重新布局消息面板
        self.conversation_panel.Layout()

    def on_close(self, event: wx.CloseEvent):
        self.save()
        event.Skip()

    def on_clear(self, event):
        self.current_conversation.clear_message()
        # 删除self.conversation_sizer中的内容
        system_msg = Message(role="system", content="you are a helpful assistant")
        self.current_conversation.add_message(system_msg)

        self.refresh_conversation_detail()

    def save(self):
        save_conversations(self.conversations, str(self.current_conversation_idx))

    def load_message(self):
        try:
            data = load_conversations()
            self.conversations = data["conversations"]
            # 0默认为没有选择或者不存在对话框，从1开始
            self.current_conversation_idx = data['current_conv_idx']
            logger.info(f"从文件中读取的当前对话框索引为: {self.current_conversation_idx}")
            if len(self.conversations):
                self.current_conversation = self.conversations[self.current_conversation_idx-1]
                if not len(self.current_conversation.messages):  # 一条消息都没有，添加一个系统消息
                    msg = Message(role="system", content="You are a helpful assistant.")
                    self.current_conversation.add_message(msg)
            else:
                # 不存在对话框的话，怎么显示 # todo 默认至少存在一个对话框
                self.current_conversation_idx = 1
                msg = Message(role="system", content="You are a helpful assistant.")
                self.current_conversation = Conversation(index=len(self.conversations)+1, messages=[msg])
                self.conversations.append(self.current_conversation)

            self.refresh_conversation_list()
            self.refresh_conversation_detail()
        except OSError:
            print("初始存储文件不存在！")
        except json.JSONDecodeError as e:
            print(repr(e), file=sys.stderr)
        except TypeError as e:
            print("初始化！")

    def start_thinking_state(self):
        # self.right_text.AppendText("\nChatGPT is thinking...")
        # 这个地方开始思考时候添加一个新的消息
        self.send_button.Disable()
        self.left_list.Disable()
        self.new_conversation_button.Disable()

    def stop_thinking_state(self):
        self.send_button.Enable()
        self.left_list.Enable()
        self.new_conversation_button.Enable()

    def on_new_conversation(self, event):
        new_conv = Conversation(index=len(self.conversations)+1)
        new_message = Message("You are a helpful assistant.", role="system")
        new_conv.add_message(new_message)

        self.conversations.append(new_conv)
        self.current_conversation = new_conv
        self.current_conversation_idx = len(self.conversations)
        self.refresh_conversation_list()
        self.refresh_conversation_detail()

    def refresh_conversation_list(self):
        conversation_titles = []
        current_idx = 0
        # todo 数组反转之后是否还能够找到当前对话框
        # todo 假设这个对话在最后，但是如果在这个对话框对话之后，立马变成第一个
        for i, conv in enumerate(reversed(self.conversations)):
            title = conv.title
            conversation_titles.append(title)
            if conv.id == self.current_conversation.id:
                current_idx = i

        self.left_list.Set(conversation_titles)

        if len(conversation_titles) > 0:
            self.left_list.SetSelection(current_idx)

    def on_send_pressed(self, event):
        self.parse_command(self.input_text.GetValue())
        self.input_text.Clear()

    def on_enter_pressed(self, event: wx.Event):
        if wx.GetKeyState(wx.WXK_SHIFT):
            event.Skip()
        else:
            self.on_send_pressed(event)

    def on_conversation_list_selected(self, event):
        selection = self.left_list.GetSelection()
        if selection != wx.NOT_FOUND:
            self.current_conversation_idx = len(self.conversations) - selection
            self.current_conversation = self.conversations[self.current_conversation_idx - 1]
            self.refresh_conversation_detail()
            logger.info(f"当前选择窗口为= : {self.current_conversation_idx}")

    def refresh_conversation_detail(self):
        """
            刷新面板，每次先删除再添加
        """
        for item in self.conversation_sizer.GetChildren():
            item.GetWindow().Destroy()
        [self.add_message_panel(msg) for msg in self.current_conversation.messages]
        self.conversation_sizer.Layout()

    def get_title_for_conversation(self, idx):
        def post_completion(resp):
            self.current_conversation.title = resp.content
            self.refresh_conversation_list()

        llm.ask(self.current_conversation.msgs_to_list(),
                post_completion,
                stream=False,
                model=self.model_list_cb.GetValue()
                )

    def unrecognized_command(self):
        """
        不能够识别的命令，将底部状态栏变为红色
        """
        self.statusbar.SetBackgroundColour('RED')
        self.statusbar.SetStatusText('Unknown Command')
        self.statusbar.Refresh()
        self.timer.Start(50)

    def parse_command(self, input_string):
        if input_string.startswith('/sw'):
            pass
        elif input_string.startswith('/nb'):
            pass
        elif input_string.startswith('/'):
            self.unrecognized_command()
            return
        else:
            new_message = Message(input_string, role="user")
            self.current_conversation.add_message(new_message)
            self.refresh_conversation_detail()

            self.start_thinking_state()
            llm.ask(self.current_conversation.msgs_to_list(),
                    and_then=self.handle_response,
                    stream=True,
                    model=self.model_list_cb.GetValue()
                    )
            return

    def on_timer(self, event):
        self.blick = self.blick + 1
        if self.blick == 25:
            self.statusbar.SetBackgroundColour('#E0E2EB')
            self.statusbar.Refresh()
            self.timer.Stop()
            self.blick = 0

    def handle_response(self, resp):
        wx.CallAfter(self.update_content, resp)
        wx.CallAfter(self.stop_thinking_state)

    def on_load_data(self):
        # 模拟耗时操作，实际应用中替换成实际的数据获取过程
        def load_data():
            return llm.model_list

        # 在后台线程中获取数据
        def background_task():
            data = load_data()
            wx.CallAfter(self.update_combo_box, data)

        threading.Thread(target=background_task).start()

    def update_combo_box(self, data):
        self.model_list_cb.SetItems(data)
        self.model_list_cb.SetSelection(0)

    """ ================按钮点击事件===================== """
    def on_settings_button_click(self, event):
        dlg = SettingsDialog(self)
        dlg.ShowModal()
        dlg.Destroy()

    def update_content(self, resp):
        current_msg = Message(role="assistant", content="")
        self.current_conversation.add_message(current_msg)
        for chunk in resp:  # todo 通过更新messages中的这个message来刷新内容
            current_msg.content += chunk.choices[0].delta.content
            # self.right_text.Clear()
            self.current_conversation.update_message(current_msg)
            self.refresh_conversation_detail()

    def on_github_button_click(self, e):
        webbrowser.open_new("https://www.baidu.com")


if __name__ == '__main__':
    app = wx.App()
    ChatClient(None, title='Wise Whisper')
    app.MainLoop()
