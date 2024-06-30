#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Time: 2024/6/25 22:10
@Author: zhengyu
@File: ollama_api
@Desc zhengyu 2024/6/25 22:10. + cause
"""
import requests
from openai import OpenAI
from whisper.logger import logger
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

    def completion(self, messages: list[dict], model=None, timeout=3):
        logger.info(f"当前使用的模型是：{model}")
        return self.client.chat.completions.create(
            model=model if model else self.model,
            messages=messages,
            stream=False,
        )

    def chat_completion(self, messages: list[dict], model=None, timeout=3):
        logger.info(f"当前使用的模型是：{model}")
        return self.client.chat.completions.create(
            model=model if model else self.model,
            messages=messages,
            stream=False,
        )

    def chat_completion_stream(self, messages: list[dict], model=None, timeout=3):
        logger.info(f"当前使用的模型是：{model}")
        return self.client.chat.completions.create(
            model=model if model else self.model,
            messages=messages,
            stream=True,
        )

    @property
    def model_list(self) -> list[str]:
        base_url = 'https://macaw-pleasing-jawfish.ngrok-free.app/api/tags'
        # 发送 GET 请求以获取模型列表
        response = requests.get(base_url)

        # 检查请求是否成功
        if response.status_code == 200:
            # 解析响应的 JSON 数据
            models = response.json()['models']
            models_list = [model['name'] for model in models]
            return models_list
        else:
            print(f"无法获取模型列表，HTTP 状态码：{response.status_code}")
            return []


def and_then(rsp):
    # 流式处理结果
    for chunk in rsp:
        print(chunk.choices[0].delta.content, end="", flush=True)


if __name__ == '__main__':
    ollama = OllamaLLM()

    # ollama.ask([{"role": "user", "content": "讲一个笑话"}], and_then)
    print(ollama.model_list)


