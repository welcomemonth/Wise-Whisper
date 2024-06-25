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
from typing import Optional
import random
import os
import sys
import json
import typing
import appdirs
import pathlib
import threading
import webbrowser

from models import ChatMessage, ConversationTree
from llm_provider.llm_openai import ask, test_llm_availability

AppDirs = appdirs.AppDirs(appname="Wise-Whisper", appauthor="zzy-yzy")


def stringify_conversation(conv: ConversationTree) -> str:
    current_conv = conv.get_current_conversation()

    if len(current_conv) == 0:
        return ""

    ret = ""
    for i, msg in enumerate(current_conv):
        speaker_str = {
            'system': "System",
            'user': "\U0001F468",
            # human_icon = "\U0001F468"
            # ai_icon = "\U0001F916"
            'assistant': "\U0001F916",
        }.get(msg.role, msg.role.capitalize())
        if i == 0:
            ret += f"{i}: <{speaker_str}>\n"
        else:
            branch_width = conv.get_branch_width(i - 1)
            child_idx = current_conv[i - 1].current_child_idx
            ret += f"{i}: <({child_idx + 1}/{branch_width}) {speaker_str}>\n"
        ret += msg.content
        if i < len(current_conv):
            ret += f"\n{'-' * 50}\n"
    return ret


def set_icon(imgpath: str, width: int = 32, height: int = 32):
    setting_icon = wx.Bitmap(imgpath, wx.BITMAP_TYPE_PNG)
    setting_icon = setting_icon.ConvertToImage()
    icon = setting_icon.Scale(width, height, wx.IMAGE_QUALITY_HIGH)  # 调整图像大小为 32x32
    return icon


def _get_next_completion_thread(conv: ConversationTree, and_then: typing.Callable, truncate_before: Optional[int]):
    if test_llm_availability():
        curr_conv = conv.get_current_conversation_as_dicts()
        if truncate_before != None:
            curr_conv = curr_conv[:truncate_before]
        completion = ask(curr_conv)
        resp = completion.choices[0].message
    else:
        resp = {
            'role': 'assistant',
            'content': f'As an AI language model, simulated response {random.randint(0, 2 ** 32)}'
        }

    and_then(resp)


def _get_title_for_conversation_thread(conv: ConversationTree, and_then: typing.Callable):
    if True:
        curr_conv = conv.get_current_conversation_as_dicts()
        if len(curr_conv) >= 3:
            messages = [
                {'role': 'system', 'content': 'Provide a short title, less than 5 words whenever possible, summarizing '
                                              'a user-submitted conversation between a user and an AI model, '
                                              'provided in JSON form. Avoid using the user\'s query verbatim in your '
                                              'title. Respond to user queries with the title you are providing, '
                                              'without other prefixes or suffixes.'},
                {'role': 'user', 'content': str(curr_conv)}
            ]
            completion = ask(messages)
            resp = completion.choices[0].message
            and_then(resp)


def get_next_completion(conv: ConversationTree, and_then: typing.Callable, truncate_before: Optional[int] = None):
    thread = threading.Thread(target=_get_next_completion_thread, args=(conv, and_then, truncate_before))
    thread.start()


def get_title_for_conversation_thread(conv: ConversationTree, and_then: typing.Callable):
    thread = threading.Thread(target=_get_title_for_conversation_thread, args=(conv, and_then))
    thread.start()


class ChatClient(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(ChatClient, self).__init__(*args, **kwargs)

        # 初始化实例属性
        self.conversations = []
        self.current_conversation = None
        self.current_conversation_idx = 0
        self.left_panel = None
        self.left_list = None
        self.new_conversation_button = None
        self.right_panel = None
        self.right_text = None
        self.input_text = None
        self.send_button = None

        self.init_ui()
        self.load()

        self.Bind(wx.EVT_CLOSE, self.on_close)
        self.SetSize((900, 600))
        self.Center()
        self.Show()

    def init_ui(self):
        self.create_left_panel()
        self.create_right_panel()

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
        setting_button.SetBitmap(set_icon("./assets/icon/cog.png"))
        setting_button.SetSize((40, 40))

        github_button = wx.Button(self.left_panel)
        github_button.SetBitmap(set_icon("./assets/icon/github.png"))
        # 给按钮绑定点击事件
        github_button.Bind(wx.EVT_BUTTON, self.on_github_button_click)

        self.new_conversation_button = wx.Button(self.left_panel, label="New")
        self.new_conversation_button.SetBitmap(set_icon("./assets/icon/plus.png"))
        self.new_conversation_button.Bind(wx.EVT_BUTTON, self.create_conversation)
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

        self.right_text = wx.TextCtrl(self.right_panel, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH2,
                                      value="Press 'New conversation' to create a new conversation.")
        self.right_text.SetMinSize((300, 300))
        font = wx.Font(wx.FontInfo(12))
        if not font.SetFaceName("Courier New"):
            font.SetFamily(wx.FONTFAMILY_TELETYPE)
        self.right_text.SetFont(font)

        # 在输入栏上方有一排按钮
        self.button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.button_sizer.Add(wx.Button(self.right_panel, label="Copy"), flag=wx.ALL, border=10)
        self.button_sizer.Add(wx.Button(self.right_panel, label="Paste"), flag=wx.ALL, border=10)
        self.button_sizer.Add(wx.Button(self.right_panel, label="Clear"), flag=wx.ALL, border=10)
        self.button_sizer.Add(wx.Button(self.right_panel, label="Find"), flag=wx.ALL, border=10)
        self.button_sizer.Add(wx.Button(self.right_panel, label="Settings"), flag=wx.ALL, border=10)

        # Create a vertical sizer for the input text and send button
        input_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.input_text = wx.TextCtrl(self.right_panel, size=(-1, 60), style=wx.TE_MULTILINE | wx.TE_PROCESS_ENTER)
        self.input_text.SetFont(font)

        self.send_button = wx.Button(self.right_panel, label="Send")
        self.send_button.Bind(wx.EVT_BUTTON, self.on_send_pressed)
        input_sizer.Add(self.input_text, 1, wx.EXPAND | wx.RIGHT | wx.LEFT | wx.BOTTOM, border=10)
        input_sizer.Add(self.send_button, 0, wx.EXPAND | wx.RIGHT | wx.LEFT | wx.BOTTOM, border=10)

        right_sizer.Add(self.right_text, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)
        right_sizer.Add(wx.StaticLine(self.right_panel), flag=wx.EXPAND | wx.RIGHT | wx.LEFT, border=10)
        right_sizer.Add(self.button_sizer, flag=wx.EXPAND)
        right_sizer.Add(input_sizer, flag=wx.EXPAND | wx.RIGHT | wx.LEFT | wx.BOTTOM, border=10)
        self.right_panel.SetSizer(right_sizer)

    def on_close(self, event: wx.CloseEvent):
        self.save()
        event.Skip()

    def save(self):
        pathlib.Path(AppDirs.user_state_dir).mkdir(parents=True, exist_ok=True)
        with open(pathlib.Path(AppDirs.user_state_dir) / 'state.dat', 'w') as f:
            json.dump({
                'conversations': [[a[0], a[1].serialize()] for a in self.conversations],
                'current_conv_idx': self.current_conversation_idx
            }, f)

    def load(self):
        try:
            with open(pathlib.Path(AppDirs.user_state_dir) / 'state.dat') as f:
                dat = json.load(f)
                self.conversations = [[a[0], ConversationTree.unserialize(a[1])] for a in dat['conversations']]
                self.current_conversation_idx = dat['current_conv_idx']
                self.current_conversation = self.conversations[self.current_conversation_idx][1]
                self.refresh_conversation_list()
                self.refresh_conversation_detail()
        except OSError:
            print("初始存储文件不存在！")
        except json.JSONDecodeError as e:
            print(repr(e), file=sys.stderr)
        except TypeError as e:
            print("初始化！")

    def start_thinking_state(self):
        self.right_text.AppendText("\nChatGPT is thinking...")
        self.send_button.Disable()
        self.left_list.Disable()
        self.new_conversation_button.Disable()

    def stop_thinking_state(self):
        self.send_button.Enable()
        self.left_list.Enable()
        self.new_conversation_button.Enable()

    def create_conversation(self, event):
        new_conv = ConversationTree()
        new_conv.add_message("system", "You are a helpful assistant.")
        self.conversations.append([f"New conversation", new_conv])
        self.current_conversation = new_conv
        self.current_conversation_idx = len(self.conversations) - 1
        self.refresh_conversation_list()
        self.refresh_conversation_detail()

    def refresh_conversation_list(self):
        conversation_titles = []
        current_idx = 0
        for i, c in enumerate(reversed(self.conversations)):
            title, conv = c
            conversation_titles.append(title)
            if self.current_conversation == conv:
                current_idx = i
        self.left_list.Set(conversation_titles)
        if len(conversation_titles) > 0:
            self.left_list.SetSelection(current_idx)

    def on_send_pressed(self, event):
        if self.current_conversation == None:
            self.create_conversation(None)
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
            self.current_conversation_idx = len(self.conversations) - 1 - selection
            self.current_conversation = self.conversations[self.current_conversation_idx][1]
            self.refresh_conversation_detail()

    def refresh_conversation_detail(self):
        self.right_text.Clear()
        self.right_text.AppendText(stringify_conversation(self.current_conversation))

    def add_to_conversation(self, role, content):
        self.current_conversation.add_message(role, content)
        self.refresh_conversation_detail()
        if self.conversations[self.current_conversation_idx][0] == "New conversation" and role == "assistant":
            self.conversations[self.current_conversation_idx][0] = "Retrieving title..."
            self.refresh_conversation_list()
            self.get_title_for_conversation(self.current_conversation_idx)

    def add_to_branch(self, sibling_level, role, content):
        if sibling_level >= 1 and sibling_level < len(self.current_conversation.get_current_conversation()):
            self.current_conversation.add_message(role, content, sibling_level - 1)
            self.refresh_conversation_detail()
            return True
        else:
            self.right_text.AppendText(
                f"\n\nrequested sibling level outside range (1 - {len(self.current_conversation.get_current_conversation())})")
            return False

    def switch_branch(self, msg_idx, branch_idx):
        try:
            self.current_conversation.change_branch(msg_idx - 1, branch_idx - 1)
            self.refresh_conversation_detail()
            return True
        except Exception as e:
            self.right_text.AppendText(f"\n\n{str(e)}")
            return False

    def role_at_level(self, msg_idx):
        curr_conv = self.current_conversation.get_current_conversation()
        if msg_idx >= 0 and msg_idx <= len(curr_conv):
            return curr_conv[msg_idx].role
        else:
            return '?'

    def new_branch(self, sibling_level, content):
        if sibling_level >= 1 and sibling_level < len(self.current_conversation.get_current_conversation()):
            if self.role_at_level(sibling_level) == 'assistant':
                self.start_thinking_state()

                def post_completion(resp):
                    wx.CallAfter(self.add_to_branch, sibling_level, resp['role'], resp['content'])
                    wx.CallAfter(self.stop_thinking_state)

                get_next_completion(self.current_conversation, post_completion, sibling_level)
            else:
                if self.add_to_branch(sibling_level, 'user', content):
                    self.start_thinking_state()

                    def post_completion(resp):
                        wx.CallAfter(self.add_to_conversation, resp['role'], resp['content'])
                        wx.CallAfter(self.stop_thinking_state)

                    get_next_completion(self.current_conversation, post_completion)
        else:
            self.right_text.AppendText(
                f"\n\nrequested sibling level for new-branch outside range (1 - {len(self.current_conversation.get_current_conversation())})")
            return False

    def new_child(self, input_string):
        self.add_to_conversation("user", input_string)
        self.start_thinking_state()

        def post_completion(resp):
            wx.CallAfter(self.add_to_conversation, resp.role, resp.content)
            wx.CallAfter(self.stop_thinking_state)

        get_next_completion(self.current_conversation, post_completion)

    def get_title_for_conversation(self, idx):
        def post_completion(resp):
            self.conversations[idx][0] = resp.content
            self.refresh_conversation_list()

        get_title_for_conversation_thread(self.conversations[idx][1], post_completion)

    def unrecognized_command(self):
        self.right_text.AppendText(
            f"\n\nunrecognized / command, try one of these instead:\n/sw a b -- switches level a message to alternative b\n/nb n str -- creates a new response at level n (str ignored when replacing ChatGPT resps)")

    def parse_command(self, input_string):
        if input_string.startswith('/sw'):
            parts = input_string.split()
            if len(parts) == 3:
                a, b = map(int, parts[1:])
                self.switch_branch(a, b)
                return
            else:
                self.unrecognized_command()
                return
        elif input_string.startswith('/nb'):
            parts = input_string.split(maxsplit=2)
            if len(parts) == 3:
                a, txt = int(parts[1]), parts[2]
                self.new_branch(a, txt)
                return
            elif len(parts) == 2:
                a = int(parts[1])
                if self.role_at_level(a) == 'assistant':
                    self.new_branch(a, None)
                else:
                    self.right_text.AppendText(
                        f"\n\nnew-branch for level {a} also requires a prompt (e.g. /nb {a} Hello, world!)")
            else:
                self.unrecognized_command()
                return
        elif input_string.startswith('/'):
            self.unrecognized_command()
            return
        else:
            self.new_child(input_string)
            return

    def on_github_button_click(self, e):
        webbrowser.open_new("https://www.baidu.com")


if __name__ == '__main__':
    app = wx.App()
    ChatClient(None, title='Wise Whisper')
    app.MainLoop()
