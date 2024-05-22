from typing import Any, Coroutine

from aiogram import Bot
from aiogram.types import Message, CallbackQuery
from aiogram.types.inaccessible_message import InaccessibleMessage

def answer_callback(
    bot: Bot,
    callback: CallbackQuery,
    **kwargs: Any
) -> Coroutine[Any, Any, Message | bool]:
    chat_id = callback.from_user.id
    message = callback.message
    
    if message is None:
        return bot.send_message(
            chat_id,
            **kwargs
        )
    else:
        return bot.edit_message_text(
            **kwargs,
            chat_id=chat_id,
            message_id=message.message_id
        )