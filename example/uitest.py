import wx


class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        super(MyFrame, self).__init__(parent, title=title, size=(600, 400))

        self.panel = wx.Panel(self)
        self.panel.SetBackgroundColour('#E8E8E8')  # 设置面板背景颜色

        # 添加布局管理
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.panel.SetSizer(self.sizer)

        # 添加一个文本框
        self.text_ctrl = wx.TextCtrl(self.panel, style=wx.TE_MULTILINE)
        self.sizer.Add(self.text_ctrl, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)

        # 添加一个按钮
        self.button = wx.Button(self.panel, label="点击我")
        self.sizer.Add(self.button, flag=wx.ALIGN_CENTER | wx.ALL, border=10)

        # 事件绑定
        self.button.Bind(wx.EVT_BUTTON, self.on_button_click)

        # 设置窗口在屏幕上的位置
        self.Centre()

    def on_button_click(self, event):
        # 在文本框中显示一条消息
        self.text_ctrl.AppendText("Hello, wxPython!\n")


# 应用程序和主窗口
app = wx.App(False)
frame = MyFrame(None, 'NextChat Example')
frame.Show()
app.MainLoop()