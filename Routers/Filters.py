from aiogram.types import Message
from aiogram.filters import BaseFilter

from keys import get_back_id

class AdminChatFilter(BaseFilter):
    def __init__(self, is_this_admin_chat: bool):
        super().__init__()
        
        self.is_this_admin_chat = is_this_admin_chat

    async def __call__(self, message: Message) -> bool:
        if self.is_this_admin_chat:
            return message.chat.id == get_back_id()
        return message.chat.id != get_back_id()
