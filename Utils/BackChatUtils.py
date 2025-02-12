import random
from aiogram import Bot
from aiogram.utils.media_group import MediaGroupBuilder

from config import config


back_send_text = """📨Новое обращение! Номер:
{0}

————

{1}

————

Статусы обращения в виде реакции на сообщение:

❤️ — возьму в работу
👍 — связались с автором обращения
🔥 — выполнили
👎 — игнорировать"""


async def send_media_to_chat(
        bot: Bot,
        chat_id: int,
        media: list[str] | str | None = None,
        caption: str | None = None
    ) -> None:
    if isinstance(media, list) and len(media) >= 1:
        media_group = MediaGroupBuilder()
        for item in media:
            media_group.add_photo(media=item, caption=caption)
        await bot.send_media_group(chat_id, media_group.build())
    elif isinstance(media, str):
        await bot.send_photo(chat_id, media, caption=caption)

async def send_files_to_chat(
        bot: Bot,
        chat_id: int,
        files: list[str] | str | None = None
    ) -> None:
    if isinstance(files, list) and len(files) >= 1:
        media_group = MediaGroupBuilder()
        for item in files:
            media_group.add_document(media=item)
        await bot.send_media_group(chat_id, media_group.build())
    elif isinstance(files, str):
        await bot.send_document(chat_id, files)

async def send_data_to_chat(
        bot: Bot,
        chat_id: int, 
        data: str,
        media: list[str] | str | None = None,
        files: list[str] | str | None = None,
        allow_caption: bool = False
    ) -> None:
    await send_media_to_chat(bot, chat_id, media, data if allow_caption else None) if media else None
    await send_files_to_chat(bot, chat_id, files) if files else None
    if not allow_caption or not media:
        await bot.send_message(chat_id, data)

async def send_request_to_back(bot: Bot, request: str, media: list[str] | str | None = None, files: list[str] | str | None = None) -> int:
    request_id = random.randint(1, 999999999)

    await send_data_to_back(bot, config.back_chat_id, back_send_text.format(request_id, request), media, files)

    return request_id
