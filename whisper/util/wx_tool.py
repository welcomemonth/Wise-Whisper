#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Time: 2024/7/1 14:24
@Author: zhengyu
@File: wx_tool
@Desc zhengyu 2024/7/1 14:24. + cause
"""
import os
import wx
from whisper.const import ICON_PATH


def set_icon(img_path: str, width: int = 16, height: int = 16):
    # 如果传入的文件路径存在则使用该路径，如果不存在则使用ICON_PATH链接路径
    if not os.path.exists(img_path):
        img_path = ICON_PATH / img_path
    if not os.path.exists(img_path):
        img_path = ICON_PATH / "error.png"
    setting_icon = wx.Bitmap(str(img_path), wx.BITMAP_TYPE_PNG)
    setting_icon = setting_icon.ConvertToImage()
    icon = setting_icon.Scale(width, height, wx.IMAGE_QUALITY_HIGH)  # 调整图像大小为 32x32
    return icon
