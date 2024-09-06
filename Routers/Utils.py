import sys

from typing import Any

from aiogram import Bot
from aiogram.types import Message, CallbackQuery, InaccessibleMessage
from aiogram.fsm.context import FSMContext


def check_if_message_has_photo(message: Message | InaccessibleMessage | None) -> bool:
    if not message or isinstance(message, InaccessibleMessage) or not message.photo:
        return False
    return True


async def answer_callback(
    bot: Bot, callback: CallbackQuery, saveMedia: bool = True, **kwargs: Any
) -> None:
    chat_id = callback.from_user.id
    message = callback.message

    message_id_to_be_deleted = None

    if message:
        is_photo_message = check_if_message_has_photo(message)

        if "photo" in kwargs and is_photo_message:
            await bot.edit_message_media(
                kwargs["media"], chat_id=chat_id, message_id=message.message_id
            )
            return
        if "photo" not in kwargs and (not is_photo_message or saveMedia):
            await bot.edit_message_text(
                **kwargs, chat_id=chat_id, message_id=message.message_id
            )
            return

        message_id_to_be_deleted = message.message_id

    if "photo" in kwargs:
        await bot.send_photo(chat_id, **kwargs)
    else:
        await bot.send_message(chat_id, **kwargs)

    if message_id_to_be_deleted:
        await bot.delete_message(chat_id, message_id_to_be_deleted)


async def try_delete_message(message: Message | InaccessibleMessage | None) -> None:
    if message and not isinstance(message, InaccessibleMessage):
        try:
            await message.delete()
        except:
            print(f'Can\'t delete message "{message.text}"', file=sys.stderr)


async def get_lang_from_state(state: FSMContext) -> str:
    try:
        data = await state.get_data()
        lang = data["language"]
        if lang not in ["ru", "en"]:
            return "ru"
        return lang
    except:
        return "ru"
