#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Time: 2024/6/24 21:10
@Author: zhengyu
@File: base_llm.py
@Desc zhengyu 2024/6/24 21:10. + create
"""
import typing
from typing import Optional, Union
from abc import ABC, abstractmethod
import threading

import openai
from openai import OpenAI

from whisper.logger import logger
from whisper.llm_config import LLMConfig


class BaseLLM(ABC):  # todo 创建一个抽象基类

    config: LLMConfig
    client: Optional[Union[OpenAI]] = None
    system_prompt = "You are a helpful assistant."

    def _assistant_msg(self, msg: str) -> dict[str, str]:
        return {"role": "assistant", "content": msg}

    def _system_msg(self, msg: str) -> dict[str, str]:
        return {"role": "system", "content": msg}

    def _system_msgs(self, msgs: list[str]) -> list[dict[str, str]]:
        return [self._system_msg(msg) for msg in msgs]

    def _default_system_msg(self):
        return self._system_msg(self.system_prompt)

    @property
    @abstractmethod
    def model_list(self):
        """
        该框架能够使用的模型列表
        """

    def ask(self, messages: list[dict[str, str]], and_then: typing.Callable, stream=False, model=None):
        """
            统一调用的接口回复问题的接口
        """
        thread = threading.Thread(target=self._ask,
                                  args=(messages, and_then),
                                  kwargs={'stream': stream, 'model': model}
                                  )
        thread.start()

    def _user_msg(self, msg: str, images: Optional[Union[str, list[str]]] = None) -> dict[str, Union[str, dict]]:
        if images:
            # as gpt-4v, chat with image
            # return self._user_msg_with_imgs(msg, images)
            return {"role": "user", "content": msg}
        else:
            return {"role": "user", "content": msg}

    def _ask(
        self,
        msg: Union[str, list[dict[str, str]]],
        and_then: typing.Callable,
        system_msgs: Optional[list[str]] = None,
        stream: bool = False,
        model: str = None
    ):
        if system_msgs:
            messages = self._system_msgs(system_msgs)
        else:
            messages = [self._default_system_msg()]

        if isinstance(msg, str):
            messages.append(self._user_msg(msg))
        else:
            messages.extend(msg)
        logger.info(messages)
        rsp = self.completion_text(messages, model=model, stream=stream)
        logger.info(rsp)
        and_then(rsp)

    @abstractmethod
    def chat_completion(self, messages: list[dict], model=None, timeout=3):
        """_achat_completion implemented by inherited class"""

    @abstractmethod
    def chat_completion_stream(self, messages: list[dict], model=None, timeout=3):
        """_achat_completion implemented by inherited class"""

    @abstractmethod
    def completion(self, messages: list[dict], model=None, timeout=3):
        """"""

    def completion_text(self, messages: list[dict], stream: bool = False, model: str = None, timeout: int = 3) -> str:
        """Asynchronous version of completion. Return str. Support stream-print"""
        if stream:
            return self.chat_completion_stream(messages, model, timeout=timeout)
        resp = self.chat_completion(messages, model, timeout=timeout)
        return self.get_choice_text(resp)

    def get_choice_text(self, rsp: openai.ChatCompletion) -> str:
        """Required to provide the first text of choice"""
        return rsp.choices[0].message.content
