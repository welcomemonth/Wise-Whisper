#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Time: 2024/6/25 15:59
@Author: zhengyu
@File: wxPython中使用多线程
@Desc zhengyu 2024/6/25 15:59. + cause
"""

import time
import datetime
import wx
from threading import Thread
from wx.lib.pubsub import pub

class TestThread(Thread):
    def __init__(self,diefu,old_data,pinlv):
        #线程实例化时立即启动
        self.diefu = diefu
        self.old_data = old_data
        self.pinlv = pinlv
        Thread.__init__(self)
        self.start()
    def run(self):
      #线程执行的代码
        while True:
            sleep = int(self.pinlv)*60
            time.sleep(sleep)
            now_time = datetime.datetime.now()
            utc_t = now_time.astimezone(tz='utc')
            utc_time = utc_t.replace(tzinfo=None)
            print(utc_time)
            if utc_time > self.time_end():
                break
            else:
                tmp = self.do_check_update(diefu,old_data)
                old_data = tmp
                self.update_json(old_data)
            wx.CallAfter(pub.sendMessage, "update", msg=i)
            time.sleep(0.5)

class MyForm ( wx.Frame ):
  def __init__( self, parent ):
    wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = "www.OmegaXYZ.com", pos = wx.DefaultPosition, size = wx.Size( -1,-1 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
    self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
    gSizer2 = wx.GridSizer( 0, 3, 0, 0 )
    self.m_button2 = wx.Button( self, wx.ID_ANY, "执行线程", wx.DefaultPosition, wx.DefaultSize, 0 )
    gSizer2.Add( self.m_button2, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )
    self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, "MyLabel", wx.DefaultPosition, wx.DefaultSize, 0 )
    self.m_staticText2.Wrap( -1 )
    gSizer2.Add( self.m_staticText2, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )
    self.m_gauge1 = wx.Gauge( self, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL )
    self.m_gauge1.SetValue( 0 )
    gSizer2.Add( self.m_gauge1, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )
    self.SetSizer( gSizer2 )
    self.Layout()
    gSizer2.Fit( self )
    self.Centre( wx.BOTH )
    self.m_button2.Bind( wx.EVT_BUTTON, self.onButton )

    pub.subscribe(self.updateDisplay, "update")
  def updateDisplay(self, msg):
    t = msg
    if isinstance(t, int):#如果是数字，说明线程正在执行，显示数字
      self.m_staticText2.SetLabel("%s%%" % t)
      self.m_gauge1.SetValue( t )
    else:#否则线程未执行，将按钮重新开启
      self.m_staticText2.SetLabel("%s" % t)
      self.m_button2.Enable()
  def onButton( self, event ):
    TestThread('1','2','3')
    self.m_staticText2.SetLabel("线程开始")
    event.GetEventObject().Disable()


if __name__ == "__main__":
  app = wx.App()
  MyForm(None).Show()
  app.MainLoop()

