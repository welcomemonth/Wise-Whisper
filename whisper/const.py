#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Time: 2024/6/24 22:35
@Author: zhengyu
@File: const.py
@Desc zhengyu 2024/6/24 22:35. + 静态变量
"""
import os
import pathlib
from pathlib import Path
import appdirs
from loguru import logger
import whisper

AppDirs = appdirs.AppDirs(appname="Wise-Whisper", appauthor="zzy-yzy")


def get_root_path():
    """Get the root directory of the installed package."""
    package_root = Path(whisper.__file__).parent.parent
    for i in (".git", ".project_root", ".gitignore"):
        if (package_root / i).exists():
            break
    else:
        package_root = Path.cwd()

    logger.info(f"Package root set to {str(package_root)}")
    return package_root


LLM_API_TIMEOUT = 300
# 项目根路径
PROJECT_ROOT = get_root_path()
CONFIG_ROOT = PROJECT_ROOT / "config"
LOG_ROOT = PROJECT_ROOT / "logs"
DATA_ROOT = pathlib.Path(AppDirs.user_data_dir)
DATA_FILE_PATH = DATA_ROOT / "state.dat"
DATA_CURRENT_INDEX = DATA_ROOT / "current_index.dat"

if __name__ == '__main__':
    print(get_root_path())
    print(CONFIG_ROOT)
    print(LOG_ROOT)
    print(DATA_ROOT)
    print(DATA_FILE_PATH)

