#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Time: 2024/6/25 15:09
@Author: zhengyu
@File: logger
@Desc zhengyu 2024/6/25 15:09. + 控制日志的打印与保存
"""

import sys

from datetime import datetime

from loguru import logger as _logger

_print_level = "INFO"


# 设置日志记录器
def setup_logger(print_level="INFO", logfile_level="DEBUG", name="app"):
    current_date = datetime.now().strftime("%Y%m%d_%H%M%S")  # 每次重新记录日志
    log_name = f"{name}_{current_date}"

    _logger.remove()
    _logger.add(sys.stderr, level=print_level)
    _logger.add(f"logs/{log_name}.log", level=logfile_level, rotation="1 MB")  # todo 日志路径问题
    return _logger



if __name__ == "__main__":
    logger = setup_logger(print_level="DEBUG", logfile_level="DEBUG")
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")



