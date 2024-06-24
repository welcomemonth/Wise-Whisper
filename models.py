'''
   Copyright 2023 Ben Z. Yuan (chatgpt-client@bzy-xyz.com)

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
'''

from __future__ import annotations
import sys


class ChatMessage:
    '''Represents a single message.
    '''
    def __init__(self, role: str, content: str, parent: ChatMessage = None):
        self.parent = parent
        self.role = role
        self.content = content
        self.children = []
        self.current_child_idx: int = 0 # used to track currently active conversation

    def add_child(self, message: ChatMessage):
        self.children.append(message)
        message.parent = self
        self.current_child_idx = len(self.children) - 1

    def to_dict(self) -> dict:
        return {
            'role': self.role,
            'content': self.content,
            'current_child_idx': self.current_child_idx
        }

    def serialize(self) -> dict:
        data = self.to_dict()
        if self.children:
            data['children'] = [child.serialize() for child in self.children]
        return data

    @classmethod
    def unserialize(cls, data: dict) -> ChatMessage:
        message = cls(data['role'], data['content'])
        if 'children' in data.keys():
            for child_data in data['children']:
                child = cls.unserialize(child_data)
                message.add_child(child)
            message.current_child_idx = data['current_child_idx']
        return message


class ConversationTree:
    '''Represents a conversation tree.
    '''
    def __init__(self):
        self.root_message: ChatMessage = None
        self.current_leaf_pointer: ChatMessage = None

    def serialize(self) -> dict:
        return self.root_message.serialize()

    @classmethod
    def unserialize(cls, data: dict) -> ConversationTree:
        ret = cls()
        ret.root_message = ChatMessage.unserialize(data)
        ret.reset_leaf_pointer()
        return ret

    def add_message(self, role: str, content: str, parent_level : int = None):
        message = ChatMessage(role, content)
        if self.root_message:
            if parent_level != None:
                current_conversation = self.get_current_conversation()
                if parent_level < len(current_conversation):
                    current_conversation[parent_level].add_child(message)
            else:
                self.current_leaf_pointer.add_child(message)
        else:
            self.root_message = message
        self.current_leaf_pointer = message

    def add_sibling_message(self, role: str, content: str):

        current_conversation = self.get_current_conversation()
        if len(current_conversation) <= 1:
            raise IndexError(f"conversation tree of depth {len(current_conversation)} doesn't support siblings")
        return self.add_message(role, content, len(current_conversation) - 2)

    def get_current_conversation(self) -> list[ChatMessage]:
        if not self.root_message:
            return []
        current_message = self.current_leaf_pointer
        conversation = []
        while current_message:
            conversation.append(current_message)
            current_message = current_message.parent
        return conversation[::-1]

    def get_current_conversation_as_dicts(self) -> list[dict]:
        return [{'role': a.role, 'content': a.content} for a in self.get_current_conversation()]

    def reset_leaf_pointer(self):
        current_message = self.root_message
        while current_message and len(current_message.children):
            current_message = current_message.children[current_message.current_child_idx]
        self.current_leaf_pointer = current_message

    def change_branch(self, level: int, idx: int):
        current_conversation = self.get_current_conversation()
        if level >= 0 and level < len(current_conversation):
            if idx >= 0 and idx < len(current_conversation[level].children):
                current_conversation[level].current_child_idx = idx
            elif len(current_conversation[level].children) > 0:
                raise IndexError(f"idx {idx} out of range for conversation level {level} (0 - {len(current_conversation[level].children) - 1})")
            else:
                raise IndexError(f"level {level} points to a leaf node!")
        else:
            raise IndexError(f"level {level} out of range for conversation (0 - {len(current_conversation) - 1})")
        # reset the current leaf pointer
        self.reset_leaf_pointer()

    def get_branch_width(self, level: int) -> int:
        current_conversation = self.get_current_conversation()
        if level >= 0 and level < len(current_conversation):
            return len(current_conversation[level].children)
        else:
            raise IndexError(f"level {level} out of range for conversation (0 - {len(current_conversation) - 1})")


if __name__ == "__main__":
    conversation_tree = ConversationTree()
    conversation_tree.add_message("system", "You are a helpful but highly verbose assistant.")
    conversation_tree.add_message("user", "Who won the world series in 2020?")

    current_conversation = conversation_tree.get_current_conversation_as_dicts()
    print(f"Current conversation tree:\n{current_conversation}")

    import os
    openai_api_key = os.getenv("OPENAI_API_KEY")
    openai_api_org = os.getenv("OPENAI_API_ORG")

    if openai_api_key:
        import openai
        if openai_api_org:
            openai.organization = openai_api_org
        openai.api_key = openai_api_key
        test_model = "gpt-3.5-turbo"
        completion = openai.ChatCompletion.create(
            model=test_model,
            messages=current_conversation,
            n=3
        )
        print(f"Completion:\n{completion}")
        for response_message in completion['choices']:
            conversation_tree.add_message(response_message['message']['role'], response_message['message']['content'], len(current_conversation) - 1)
    else:
        print(f"Set OPENAI_API_KEY and OPENAI_API_ORG to try querying the OpenAI API.")
        print(f"Simulating a query outcome...")
        conversation_tree.add_message("assistant", "Test response 1", len(current_conversation) - 1)
        conversation_tree.add_message("assistant", "Test response 2", len(current_conversation) - 1)
        conversation_tree.add_message("assistant", "Test response 3", len(current_conversation) - 1)


    level = len(current_conversation) - 1
    for b in range(conversation_tree.get_branch_width(level)):
        print(f"Switching to branch {b}")
        conversation_tree.change_branch(level, b)
        current_conversation = conversation_tree.get_current_conversation_as_dicts()
        print(f"Current conversation tree:\n{current_conversation}")