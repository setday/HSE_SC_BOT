from typing import Any, Coroutine

from aiogram import Bot
from aiogram.types import Message, CallbackQuery


def answer_callback(
    bot: Bot, callback: CallbackQuery, **kwargs: Any
) -> Coroutine[Any, Any, Message | bool]:
    chat_id = callback.from_user.id
    message = callback.message

    if message is None:
        return bot.send_message(chat_id, **kwargs)
    else:
        return bot.edit_message_text(
            **kwargs, chat_id=chat_id, message_id=message.message_id
        )

async def get_lang_from_state(state: any) -> str:
    try:
        data = await state.get_data()
        lang = data["language"]
        if lang not in ["ru", "en"]:
            return "ru"
        return lang
    except:
        return "ru"
