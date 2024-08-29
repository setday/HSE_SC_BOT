from typing import Any
from aiogram.types import Message
from aiogram.filters import BaseFilter

from keysLoader import get_back_id


class AdminChatFilter(BaseFilter):
    def __init__(self, is_this_admin_chat: bool = True):
        super().__init__()

        self.is_this_admin_chat = is_this_admin_chat

    async def __call__(self, message: Message) -> bool:
        if self.is_this_admin_chat:
            return message.chat.id == get_back_id()
        return message.chat.id != get_back_id()

class VoteChatFilter(BaseFilter):
    def __init__(self, is_this_admin_chat: bool = True):
        super().__init__()

        self.is_this_admin_chat = is_this_admin_chat

    async def __call__(self, message: Message) -> bool:
        if self.is_this_admin_chat:
            return message.chat.id == get_back_id()
        return message.chat.id != get_back_id()
    
class SuperChatFilter(BaseFilter):
    def __init__(self, is_this_admin_chat: bool = True):
        super().__init__()

        self.is_this_admin_chat = is_this_admin_chat

    async def __call__(self, message: Message) -> bool:
        if self.is_this_admin_chat:
            return message.chat.id == get_back_id() or message.chat.id == get_back_id()
        return message.chat.id != get_back_id() and message.chat.id != get_back_id()
    
class WordDocFilter(BaseFilter):
    def __init__(self) -> None:
        super().__init__()

    async def __call__(self, message: Message) -> bool:
        return message.document is not None and message.document.mime_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
