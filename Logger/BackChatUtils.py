import random

from aiogram import Bot

from keys import get_back_id

async def send_data_to_back(bot: Bot, data: str) -> int:
    number = random.randint(1, 9999999)

    await bot.send_message(get_back_id(), f"({number})\n\n{data}")

    return number
