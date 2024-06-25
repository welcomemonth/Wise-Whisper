#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Time: 2024/6/24 21:23
@Author: zhengyu
@File: llm_config
@Desc zhengyu 2024/6/24 21:23. + cause
"""

from enum import Enum
from typing import Optional

from pydantic import field_validator

from config.const import LLM_API_TIMEOUT


class LLMType(Enum):
    OPENAI = "openai"
    AZURE = "azure"
    OLLAMA = "ollama"
    CLAUDE = "claude"

    """
    在Python中，方法是一个特殊方法，它定义在字典（`dict`）或其子类中。当你尝试通过键来访问字典中的元素，但这个键在字典中不存在时，方法会被调用。这为处理缺失的键提供了一种优雅的方式。
    在你提供的代码片段中，[`__missing__`]方法被定义在一个类中（假设这个类是`dict`的子类）。这个方法接受一个参数[`key`]，这个参数是尝试访问但在字典中找不到的键。方法的实现非常简单：无论哪个键缺失，它总是返回[`self.OPENAI`]。
    这意味着，如果你的这个类的实例尝试访问任何不存在的键，不会像通常的字典那样抛出`KeyError`异常，而是会返回这个类实例中[`OPENAI`]属性的值。这可以用于提供默认值，或者在某些特定的键缺失时返回一个特定的值。
    这种做法在需要对缺失的键进行统一处理时非常有用，比如在配置管理中，当某些配置项未被明确设置时，你可能希望返回一个默认的配置值。在这个例子中，不管哪个键缺失，都会返回[`OPENAI`]属性的值，这可能是一个默认的配置值或者一个占位符。
    """

    def __missing__(self, key):
        return self.OPENAI


class LLMConfig:
    """

    """

    api_key: str = "sk-"
    api_type: LLMType = LLMType.OPENAI
    base_url: str = "https://api.openai.com/v1"
    api_version: Optional[str] = None

    model: Optional[str] = None  # also stands for DEPLOYMENT_NAME
    pricing_plan: Optional[str] = None  # Cost Settlement Plan Parameters.

    # For Cloud Service Provider like Baidu/ Alibaba
    access_key: Optional[str] = None
    secret_key: Optional[str] = None
    endpoint: Optional[str] = None  # for self-deployed model on the cloud

    # For Spark(Xunfei), maybe remove later
    app_id: Optional[str] = None
    api_secret: Optional[str] = None
    domain: Optional[str] = None

    # For Chat Completion
    max_token: int = 4096
    temperature: float = 0.0
    top_p: float = 1.0
    top_k: int = 0
    repetition_penalty: float = 1.0
    stop: Optional[str] = None
    presence_penalty: float = 0.0
    frequency_penalty: float = 0.0
    best_of: Optional[int] = None
    n: Optional[int] = None
    stream: bool = False
    logprobs: Optional[bool] = None  # https://cookbook.openai.com/examples/using_logprobs
    top_logprobs: Optional[int] = None
    timeout: int = 600

    # For Network
    proxy: Optional[str] = None

    # Cost Control
    calc_usage: bool = True

    @field_validator("api_key")
    @classmethod
    def check_llm_key(cls, v):
        if v in ["", None, "YOUR_API_KEY"]:
            raise ValueError("Please set your API key in config2.yaml")
        return v

    @field_validator("timeout")
    @classmethod
    def check_timeout(cls, v):
        return v or LLM_API_TIMEOUT
