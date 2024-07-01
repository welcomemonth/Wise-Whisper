import wx
import wx.html2
import wx.lib.scrolledpanel as scrolled
import markdown
from whisper.schema import Message
from whisper.util import set_icon


class MessagePanel(wx.Panel):
    def __init__(self, parent, message):
        super().__init__(parent)

        content = message.content
        timestamp = message.created_at

        # 创建头像
        icon_image = set_icon('robot.png', 32, 32)
        avatar = wx.StaticBitmap(self, bitmap=icon_image)

        # 渲染Markdown内容
        self.message_html = wx.html2.WebView.New(self)
        self.md2html(content)

        # 创建消息文本
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
        text_sizer.Add(self.message_html, proportion=0, flag=wx.ALL | wx.EXPAND, border=5)
        text_sizer.Add(self.timestamp_text, flag=wx.ALL, border=5)

        top_sizer.Add(text_sizer, proportion=1, flag=wx.EXPAND)

        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        button_sizer.Add(copy_button, flag=wx.ALL, border=5)
        button_sizer.Add(edit_button, flag=wx.ALL, border=5)
        button_sizer.Add(refresh_button, flag=wx.ALL, border=5)
        button_sizer.Add(pin_button, flag=wx.ALL, border=5)

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(top_sizer, proportion=0, flag=wx.EXPAND)
        main_sizer.Add(button_sizer, flag=wx.ALIGN_LEFT | wx.LEFT, border=40)

        self.SetSizer(main_sizer)
        self.Fit()  # 调整面板大小以适应内容

        # 保存消息内容
        self.content = content

    def set_content(self, content):
        self.md2html(content)
        self.adjust_height()

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
            self.set_content(self.content)
        dialog.Destroy()

    def on_refresh(self, event):
        wx.MessageBox("消息已刷新", "信息", wx.OK | wx.ICON_INFORMATION)

    def on_pin(self, event):
        wx.MessageBox("消息已固定", "信息", wx.OK | wx.ICON_INFORMATION)


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
        小腿的“瘦腿”过程需要时间和耐心，通过合理饮食、适量运动和按摩相结合的方式，可以逐渐看到效果。""", role="assistant")

        self.add_message(msg1)
        self.add_message(msg2)
        self.add_message(msg3)
        self.add_message(msg4)

    def add_message(self, message):
        message_panel = MessagePanel(self.message_panel, message)
        self.message_sizer.Add(message_panel, flag=wx.EXPAND | wx.ALL, border=5)
        self.message_panel.Layout()
        self.message_panel.FitInside()

        # 调整父容器大小以适应内容
        self.conversation_panel.Layout()
        self.conversation_panel.GetSizer().Layout()


if __name__ == "__main__":
    app = wx.App(False)
    frame = ConversationFrame()
    frame.Show()
    app.MainLoop()

