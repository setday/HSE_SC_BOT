import random
from  datetime import datetime
import re
import os

from docx import Document

from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.state import State

from ..Filters import VoteChatFilter, WordDocFilter, SuperChatFilter

from Routers.KeyboardMaker import make_back_to_main_menu_keyboard

from .ExtraRouterInfo import *


def get_dead_list(file):
    res = []

    doc = Document(file)
    for para in doc.paragraphs:
        re_res = re.findall(r"римен.ть в отношении студент.*мер. дисциплинарного взыскания", para.text)
        for r in re_res:
            res.append(r[30:-31].strip())

    return res


class ExtraRouter(Router):
    def __init__(self, bot: Bot) -> None:
        super().__init__()

        self.bot = bot

        self.message.register(self.get_chat_id_handler, Command("chat_id"))
        self.message.register(self.get_state_handler, Command("get_state"))
        self.message.register(self.get_fact_handler, Command("fact"))
        self.message.register(self.create_mm_poll_handler, VoteChatFilter(), WordDocFilter())

    async def get_chat_id_handler(self, message: Message) -> None:
        await message.answer(chat_id_text.format(message.chat.id), reply_markup=make_back_to_main_menu_keyboard())
        await message.delete()

    async def get_state_handler(self, message: Message, state: State) -> None:
        await message.answer(state_text.format(str(state)), reply_markup=make_back_to_main_menu_keyboard())
        await message.delete()

    datetime_event_start = datetime(year=2024, month=1, day=19, hour=4, minute=4, microsecond=0)
    secret_trash = os.getenv("SECRET_TRASH")

    async def get_fact_handler(self, message: Message) -> None:
        if datetime.today().replace(microsecond=0, second=0, month=1) == self.datetime_event_start and \
            message.from_user and \
            message.from_user.username and \
            self.secret_trash:

            user_hash = hash(message.from_user.username + self.secret_trash)
            await message.answer(facts_format_text.format('?') + facts_text[0].format(user_hash), reply_markup=make_back_to_main_menu_keyboard())
            await message.delete()

            return

        fact_id = random.randint(1, len(facts_text))

        await message.answer(facts_format_text.format(fact_id) + facts_text[fact_id], reply_markup=make_back_to_main_menu_keyboard())
        await message.delete()

    async def create_mm_poll_handler(self, message: Message) -> None:
        if not message.document:
            return
        
        file = await self.bot.download(message.document.file_id)
        if file is None:
            return
        
        dead_list = get_dead_list(file)
        print(dead_list)
        file.close()
        
        for dead in dead_list:
            await message.answer_poll(
                question=dead+"?",
                options=[
                    "Устное замечание",
                    "Замечание",
                    "Выговор",
                    "Отчисление",
                    "Против мер дисциплинарного взыскания",
                    "Воздержаться",
                ],
                is_anonymous=False,
                allows_multiple_answers=False,
            )
