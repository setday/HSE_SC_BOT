import random
from datetime import datetime
import re
import os

from docx import Document

from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import User

from Utils.Filters import VoteChatFilter, WordDocFilter, SuperChatFilter, AdminChatFilter

from Utils.KeyboardMaker import make_back_to_main_menu_keyboard

from .ExtraRouterTexts import *

from Utils.Utils import try_delete_message


def get_dead_list(file):
    res = []

    doc = Document(file)
    for para in doc.paragraphs:
        re_res = re.findall(
            r"римен.ть в отношении студент..? .* мер.? дисциплинарного взыскания",
            para.text,
        )
        for r in re_res:
            r = r.split(" ", 4)[4]
            r = r.rsplit(" ", 3)[0]
            res.append(r)

    return res


class ExtraRouter(Router):
    def __init__(self, bot: Bot) -> None:
        super().__init__()

        self.bot = bot
        self.bot_info: User | None = None

        self.message.register(self.get_chat_id_handler, Command("chat_id"))
        self.message.register(self.get_bot_id_handler, Command("bot_id"))
        self.message.register(self.get_state_handler, Command("get_state"))

        self.message.register(self.get_credits_handler, Command("credits"))
        self.message.register(self.get_fact_handler, Command("fact"))
        self.message.register(self.del_handler, Command("del"))
        self.message.register(
            self.create_mm_poll_handler, VoteChatFilter(True), WordDocFilter()
        )
        self.message.register(self.answer_user, AdminChatFilter(), Command("answer"))

    async def get_chat_id_handler(self, message: Message) -> None:
        await message.answer(
            chat_id_text.format(message.chat.id),
            reply_markup=make_back_to_main_menu_keyboard(),
        )

    async def get_bot_id_handler(self, message: Message) -> None:
        if not self.bot_info:
            self.bot_info = await self.bot.get_me()
        await message.answer(
            bot_id_text.format(self.bot_info.id),
            reply_markup=make_back_to_main_menu_keyboard(),
        )

    async def get_state_handler(self, message: Message, state: FSMContext) -> None:
        state_text = await state.get_state() or "None"
        data_text = await state.get_data() or "None"

        await message.answer(
            fsm_state_text.format(state_text, data_text),
            reply_markup=make_back_to_main_menu_keyboard(),
        )

    async def get_credits_handler(self, message: Message) -> None:
        await message.answer(
            credits_text,
            reply_markup=make_back_to_main_menu_keyboard(),
        )

    datetime_event_start = datetime(
        year=2024, month=1, day=19, hour=4, minute=4, microsecond=0
    )
    secret_trash = os.getenv("SECRET_TRASH")

    async def get_fact_handler(self, message: Message) -> None:
        if (
            datetime.today().replace(microsecond=0, second=0, month=1)
            == self.datetime_event_start
            and message.from_user
            and message.from_user.username
            and self.secret_trash
        ):

            user_hash = hash(message.from_user.username + self.secret_trash)
            await message.answer(
                facts_format_text.format("?") + facts_text[0].format(user_hash),
                reply_markup=make_back_to_main_menu_keyboard(),
            )

            return

        fact_id = random.randint(1, len(facts_text) - 1)

        await message.answer(
            facts_format_text.format(fact_id) + facts_text[fact_id],
            reply_markup=make_back_to_main_menu_keyboard(),
        )

    async def create_mm_poll_handler(self, message: Message) -> None:
        print("New vote candidate", message.document)
        if not message.document:
            return

        file = await self.bot.download(message.document.file_id)
        print(file)
        if file is None:
            return

        dead_list = get_dead_list(file)
        print(dead_list)
        file.close()

        for dead in dead_list:
            await message.answer_poll(
                question="ММ " + dead,
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

    async def del_handler(self, message: Message) -> None:
        if not self.bot_info:
            self.bot_info = await self.bot.get_me()
        if (
            not message.reply_to_message
            or not message.reply_to_message.from_user
            or message.reply_to_message.from_user.id != self.bot_info.id
        ):
            return
        await try_delete_message(message.reply_to_message)
        await try_delete_message(message)

    async def answer_user(self, message: Message) -> None:
        if not message.text:
            return
        
        parts = message.text.split(maxsplit=2)

        if len(parts) < 3:
            await message.answer("Команда должна быть в формате `/answer [user id] [text]`", parse_mode="Markdown")
            return

        user_id = parts[1]
        if not user_id.isdigit():
            await message.answer("Команда должна быть в формате `/answer [user id] [text]`. `[user id]` должен быть числом", parse_mode="Markdown")
            return
        text = parts[2]

        print(user_id, text)
        
        await self.bot.send_message(user_id, f"Сообщение по одному из ваших обращений:\n\n{text}")
        await message.answer(f"Ответ отправлен пользователю {user_id}")
