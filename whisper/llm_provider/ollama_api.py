#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Time: 2024/6/25 22:10
@Author: zhengyu
@File: ollama_api
@Desc zhengyu 2024/6/25 22:10. + cause
"""
from openai import OpenAI

from whisper.llm_config import LLMConfig, CONFIG
from whisper.llm_provider.base_llm import BaseLLM


class OllamaLLM(BaseLLM):

    def __init__(self, config: LLMConfig = None):
        if config is None:
            config = CONFIG
        self.__init_ollama(config)
        self.config = config
        self.client = OpenAI(
            base_url=config.base_url,
            api_key='ollama'  # required, but unused
        )

    def __init_ollama(self, config: LLMConfig):
        assert config.base_url, "ollama base url is required!"
        self.model = config.model
        self.pricing_plan = self.model

    def completion(self, messages: list[dict], timeout=3):
        return self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            stream=False,
        )

    def chat_completion(self, messages: list[dict], timeout=3):
        return self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            stream=False,
        )

    def chat_completion_stream(self, messages: list[dict], timeout=3):
        return self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            stream=True,
        )


def and_then(rsp):
    # 流式处理结果
    for chunk in rsp:
        print(chunk.choices[0].delta.content, end="", flush=True)


if __name__ == '__main__':
    ollama = OllamaLLM()

    ollama.ask([{"role": "user", "content": "讲一个笑话"}], and_then)


