import random
from aiogram import Bot

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


async def send_data_to_back(bot: Bot, data: str):
    await bot.send_message(config.back_chat_id, data)

async def send_request_to_back(bot: Bot, request: str) -> int:
    request_id = random.randint(1, 999999999)

    await send_data_to_back(bot, back_send_text.format(request_id, request))

    return request_id
