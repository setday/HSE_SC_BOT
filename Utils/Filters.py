from aiogram.types import Message, CallbackQuery
from aiogram.filters import BaseFilter

from config import config


class AdminChatFilter(BaseFilter):
    def __init__(self, is_this_admin_chat: bool = True):
        super().__init__()

        self.is_this_admin_chat = is_this_admin_chat

    async def __call__(self, message: Message | CallbackQuery) -> bool:
        if isinstance(message, CallbackQuery):
            return True

        if self.is_this_admin_chat:
            return message.chat.id == config.back_chat_id
        return message.chat.id != config.back_chat_id
