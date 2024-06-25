#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Time: 2024/6/25 14:40
@Author: zhengyu
@File: schema
@Desc zhengyu 2024/6/25 14:40. + 设计消息格式
"""

import asyncio
import json
import os.path
import uuid

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    PrivateAttr,
    field_serializer,
    field_validator,
    model_serializer,
    model_validator,
)
from typing import Any, Dict, Iterable, List, Optional, Type, TypeVar, Union

# ChatCompletionChunk(id='chatcmpl-263', choices=[Choice(delta=ChoiceDelta(content='OK', function_call=None, role='assistant', tool_calls=None), finish_reason=None, index=0, logprobs=None)], created=1719298104, model='llama2:13b', object='chat.completion.chunk', service_tier=None, system_fingerprint='fp_ollama', usage=None)
# ChatCompletion(id='chatcmpl-376', choices=[Choice(finish_reason='stop', index=0, logprobs=None, message=ChatCompletionMessage(content="Okay! Here's a cold one for you:\n\nWhy did the tomato turn down the date with the avocado?\n\nBecause it was a fruit-less relationship! 😜", role='assistant', function_call=None, tool_calls=None))], created=1719298206, model='llama2:13b', object='chat.completion', service_tier=None, system_fingerprint='fp_ollama', usage=CompletionUsage(completion_tokens=47, prompt_tokens=0, total_tokens=47))


class Message(BaseModel):
    """

    """

    id: str = Field(default="", validate_default=True)
    role: str = "user"  # system / user / assistant
    content: str = ""

    @field_validator("id", mode="before")
    @classmethod
    def check_id(cls, id: str) -> str:
        return id if id else uuid.uuid4().hexc

