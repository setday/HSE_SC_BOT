from datetime import datetime, timedelta
import pytz
import sys

from typing import Any

from aiogram import Bot
from aiogram.types import Message, CallbackQuery, InaccessibleMessage
from aiogram.fsm.context import FSMContext
from aiogram.types import InputMediaPhoto, InputFile


def check_if_message_has_photo(message: Message | InaccessibleMessage | None) -> bool:
    if not message:
        return False
    if isinstance(message, InaccessibleMessage):
        return False
    return message.content_type != "text"

def check_if_date_has_expired(message: Message | InaccessibleMessage | None) -> bool:
    if not message:
        return True
    if isinstance(message, InaccessibleMessage):
        return True
    return message.date + timedelta(hours=48) < datetime.now(pytz.UTC)


async def answer_callback(
    bot: Bot,
    callback: CallbackQuery,
    text: str | None = None,
    photo: InputFile | None = None,
    saveMedia: bool = True,
    **kwargs: Any
) -> None:
    if text and len(text) > 1024:
        saveMedia = False
        photo = None

    chat_id = callback.from_user.id
    message = callback.message

    message_has_media = check_if_message_has_photo(message)
    data_has_media = photo is not None

    should_message_be_changed = (not message_has_media and data_has_media) or (not saveMedia and message_has_media and not data_has_media)

    message_is_dead = check_if_date_has_expired(message)
    if message_is_dead:
        message = None

    if should_message_be_changed or message is None:
        if data_has_media:
            await bot.send_photo(chat_id, caption=text, photo=photo, **kwargs)
        else:
            await bot.send_message(chat_id, text=(text or ""), **kwargs)

        if message:
            try:
                await bot.delete_message(chat_id, message.message_id)
            except:
                print(f'Can\'t delete message', file=sys.stderr)
        
        return

    if message_has_media:
        if data_has_media:
            await bot.edit_message_media(
                media=InputMediaPhoto(media=photo),
                chat_id=chat_id,
                message_id=message.message_id
            )
        await bot.edit_message_caption(
            caption=text,
            chat_id=chat_id,
            message_id=message.message_id,
            **kwargs,
        )
    elif text:
        await bot.edit_message_text(
            text=text,
            chat_id=chat_id,
            message_id=message.message_id,
            **kwargs,
        )


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
