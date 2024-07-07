import random

from aiogram import Bot

from keys import get_back_id

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


async def send_data_to_back(bot: Bot, data: str) -> int:
    number = random.randint(1, 9999999)

    await bot.send_message(get_back_id(), back_send_text.format(number, data))

    return number
