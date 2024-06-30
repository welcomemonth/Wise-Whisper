#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Time: 2024/6/25 14:40
@Author: zhengyu
@File: schema
@Desc zhengyu 2024/6/25 14:40. + 设计消息格式
"""

import json
import os.path
import pathlib
import uuid
from datetime import datetime

from whisper.const import DATA_FILE_PATH, DATA_CURRENT_INDEX

from pydantic import (
    BaseModel,
    Field,
    field_validator,
)
from typing import Any, List, Optional, Union

from whisper.logger import logger


class Message(BaseModel):
    """

    """

    id: str = Field(default="", validate_default=True)
    role: str = "user"  # system / user / assistant
    content: str = ""
    created_at: str = Field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    def __init__(self, content: str = "", **data: Any):
        data["content"] = data.get("content", content)
        super().__init__(**data)

    @field_validator("id", mode="before")
    @classmethod
    def check_id(cls, id: str) -> str:
        return id if id else uuid.uuid4().hex

    def formatted_content(self, index: int, total: int) -> str:
        speaker_str = {
            'system': "System",
            'user': "\U0001F468",
            'assistant': "\U0001F916",
        }.get(self.role, "Unknown")
        if index == 0:
            ret = f"{index}: <{speaker_str}>\n"
        else:
            ret = f"{index}: <({index + 1}/{total}) {speaker_str}>\n"
        ret += self.content
        ret += f"\n{'-' * 50}\n"
        return ret


class SimpleMessage(BaseModel):
    content: str
    role: str


class Conversation(BaseModel):

    id: str = Field(default="", validate_default=True)
    messages: List[Message] = []
    title: str = "new conversation"
    created_at: str = Field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    index: int = 0  # 当前对话框在列表中的索引

    @field_validator("id", mode="before")
    @classmethod
    def check_id(cls, id: str) -> str:
        return id if id else uuid.uuid4().hex

    # @property
    # def formatted_created_at(self) -> str:
    #     return self.created_at.strftime("%Y-%m-%d %H:%M:%S")

    def msgs_to_list(self) -> list[dict[str, str]]:
        """
        将这个对话框的所有消息内容转换成SimpleMessage列表
        """
        return [{"role": m.role, "content": m.content} for m in self.messages]

    def stringify_conversation(self) -> str:
        """
        将这个对话框的所有内容拼成一个JSON字符串
        """
        conversation_dict = self.dict()
        return json.dumps(conversation_dict, ensure_ascii=False)

    def add_message(self, message: Message):
        self.messages.append(message)

    def update_message(self, message: Message, index: int = -1):
        self.messages[index] = message

    def formatted_conversation(self) -> str:
        ret = ""
        total = len(self.messages)
        for i, message in enumerate(self.messages):
            ret += message.formatted_content(i, total)
        return ret

    def clear_message(self):
        self.messages = []

def save_conversations(cons: List[Conversation], current_idx: str):
    """
    将对话框列表保存到文件中
    """
    talk_data = []
    for talk in cons:
        talk_dict = talk.dict()
        talk_data.append(talk_dict)

    talk_json = json.dumps(talk_data, ensure_ascii=False, separators=(',', ':'))
    try:
        with open(DATA_FILE_PATH, "w", encoding='utf-8') as file:
            file.write(talk_json)
        with open(DATA_CURRENT_INDEX, "w", encoding='utf-8') as file:
            file.write(str(current_idx))

        logger.info("Conversations saved to file.")
    except OSError:
        logger.error("Failed to save conversations to file.")
    except Exception as e:
        logger.error(f"An error occurred while saving conversations: {e}")


def load_conversations() -> Union[dict[str, Union[list[Any], int]], list[Conversation]]:
    """
    从文件中读取对话框列表
    """
    if not os.path.exists(DATA_FILE_PATH):  # todo 修改为全局变量
        return {"conversations": [], "current_conv_idx": 0}

    if not os.path.exists(DATA_CURRENT_INDEX):  # todo 修改为全局变量
        current_index = 0
    else:
        with open(DATA_CURRENT_INDEX, "r", encoding='utf-8') as file:
            content = file.read()
            logger.info(f"Current content: {content}")
            # todo 判断文件中读到的是否是一个可转换为整数的字符串
            current_index = 0 if content == "" else int(content)

    # 从文件中读取 JSON 字符串并解析为对话框列表
    with open(DATA_FILE_PATH, "r", encoding='utf-8') as file:
        loaded_conversations_json = file.read()
        # logger.info(f"当前消息内容为: {loaded_conversations_json}")

    # 可能出现文件为空的情况，这种情况json解析失败
    try:
        loaded_conversations_data = json.loads(loaded_conversations_json)
    except Exception as e:
        logger.debug(f"读取文件出现错误：{e}")
        return {"conversations": [], "current_conv_idx": 0}
    # 根据加载的数据创建 Conversation 对象列表
    loaded_conversations = []
    for index, conv_data in enumerate(loaded_conversations_data):
        conv = Conversation(**conv_data)
        loaded_conversations.append(conv)

    return {"conversations": loaded_conversations, "current_conv_idx": current_index}


if __name__ == "__main__":
    msg = Message("你好", role="assistant", index=10)
    conv1 = Conversation()
    conv1.add_message(msg)
    print(conv1)
    # 创建一个Conversation对象
    # conv2 = Conversation(
    #     id="123",
    #     messages=[
    #         Message(content="Hello", role="user"),
    #         Message(content="Hi there", role="assistant")
    #     ],
    #     title="Sample Conversation"
    # )
    # conversations_data = []
    # conversations = [conv1, conv2]
    # # save_conversations(conversations, "123")
    # logger.info(load_conversations())
