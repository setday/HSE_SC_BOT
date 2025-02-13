import random
from datetime import datetime
import re

from docx import Document

from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import BaseStorage
from aiogram.types import User

from config import config

from Utils.Filters import AdminChatFilter

from Utils.KeyboardMaker import make_back_to_main_menu_keyboard, make_keyboard

from .ExtraRouterTexts import *

from Utils.Utils import try_delete_message, get_lang_from_state
from Utils.BotStorage import BotStorage

from Routers.Events.valentinesDay.ValentinesDayRouter import ValentinesDayRouter


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

        self.event_router = None

        self.bot = bot
        self.bot_info: User | None = None

        self.message.register(self.get_chat_id_handler, Command("chat_id"))
        self.message.register(self.get_bot_id_handler, Command("bot_id"))
        self.message.register(self.get_state_handler, Command("get_state"))

        self.message.register(self.start_event_handler, AdminChatFilter(), Command("start_event"))
        self.message.register(self.stop_event_handler, AdminChatFilter(), Command("stop_event"))

        self.message.register(self.make_approval_message, AdminChatFilter(), Command("valentine_news"))
        self.callback_query.register(self.approve_command, AdminChatFilter(), F.data == "approve")
        self.callback_query.register(self.decline_command, AdminChatFilter(), F.data == "decline")

        self.message.register(self.get_credits_handler, Command("credits"))
        self.message.register(self.get_fact_handler, Command("fact"))
        self.message.register(self.del_handler, Command("del"))
        self.message.register(self.answer_user, AdminChatFilter(), Command("ans"))

        self._reload_assets_callback = None

    async def execute_command(self, command: str, storage: BaseStorage) -> str:
        parts = command.split()
        cmd = parts[0]

        match cmd:
            case "/start_event":
                config.activate_event(parts[1])
                if self._reload_assets_callback:
                    self._reload_assets_callback()

                if parts[1] == "valentines_day":
                    self.event_router = ValentinesDayRouter(self.bot)
                    self.include_router(self.event_router)

                return f"Событие {parts[1]} запущено"
            
            case "/stop_event":
                config.activate_event(None)
                if self._reload_assets_callback:
                    self._reload_assets_callback()

                if self.event_router and self.event_router.parent_router:
                    self.event_router.parent_router.sub_routers.remove(self.event_router)
                self.event_router = None

                return f"Все события остановлены"
            
            case "/valentine_news":
                if not self.event_router:
                    return f"Сначала запустите событие valentines_day"
                
                await self.event_router.post.broadcast_message(storage)

                return f"Рассылка новостного поста 14 февраля запущена"
            
            case _:
                return f"Команда {cmd} не найдена"

    async def make_approval_message(self, message: Message, state: FSMContext, min_approval_count: int = 1) -> None:
        if not message.text or not message.from_user:
            return

        await self.bot.send_message(
            message.chat.id,
            approval_text.format(command=message.text, user_name=message.from_user.full_name, user_id=message.from_user.id, min_approval_count=min_approval_count),
            reply_markup=make_keyboard(("✅", "approve"), ("❌", "decline")),
        )

    async def approve_command(self, callback: CallbackQuery, state: FSMContext) -> None:
        if not callback.message or not isinstance(callback.message, Message) or not callback.message.text:
            return
        
        if str(callback.from_user.id) in callback.message.text:
            await callback.answer("Вы уже одобрили эту команду")
            return
        
        await callback.answer("Команда одобрена")

        lptr = callback.message.text.rfind("[")
        rptr = callback.message.text.rfind("]")
        
        left_count = int(callback.message.text[lptr + 1 : rptr]) - 1
        lpart = callback.message.text[:lptr]
        rpart = callback.message.text[rptr + 1 :]
        
        if left_count == 0:
            command = callback.message.text.split("\n", 1)[0]
            await callback.message.edit_text(
                f"Команда {command} откправлена на исполнение"
            )
            result = await self.execute_command(command, state.storage)
            await callback.message.edit_text(result)
            return

        newtext = f"{lpart}[{left_count}]{rpart}\n{callback.from_user.full_name}|{callback.from_user.id}"

        await callback.message.edit_text(
            newtext,
            reply_markup=make_keyboard(("✅", "approve"), ("❌", "decline")),
        )

    async def decline_command(self, callback: CallbackQuery) -> None:
        if not callback.message or not isinstance(callback.message, Message) or not callback.message.text:
            return
        
        await callback.answer("Команда отклонено")
        
        await callback.message.edit_text(
            f"{callback.message.text}\n\n{callback.from_user.full_name}|{callback.from_user.id} отклонил команду",
        )

    def set_reload_assets_callback(self, callback) -> None:
        self._reload_assets_callback = callback

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

    async def start_event_handler(self, message: Message, state: FSMContext) -> None:
        if not message.text:
            return

        parts = message.html_text.split(maxsplit=1)
        if len(parts) == 1:
            await message.answer(
                "Команда должна быть в формате `/start_event [valentines_day]`",
                parse_mode="Markdown",
            )
            return
        
        event_name = parts[1]

        if event_name not in ["valentines_day"]:
            await message.answer(
                "Событие не найдено",
                parse_mode="Markdown",
            )
            return

        await self.make_approval_message(message, state)

    async def stop_event_handler(self, message: Message, state: FSMContext) -> None:
        if not message.text:
            return

        parts = message.html_text.split(maxsplit=1)
        if len(parts) == 1:
            await self.make_approval_message(message, state)

            return
        
        event_name = parts[1]

        if event_name not in ["valentines_day"]:
            await message.answer(
                "Событие не найдено",
                parse_mode="Markdown",
            )
            return

        await self.make_approval_message(message, state)

    async def get_credits_handler(self, message: Message, state: FSMContext) -> None:
        lang = await get_lang_from_state(state)

        await message.answer(
            credits_text[lang],
            reply_markup=make_back_to_main_menu_keyboard(),
        )

    datetime_event_start = datetime(
        year=2024, month=1, day=19, hour=4, minute=4, microsecond=0
    )

    async def get_fact_handler(self, message: Message, state: FSMContext) -> None:
        lang = await get_lang_from_state(state)

        if (
            datetime.today().replace(microsecond=0, second=0, month=1)
            == self.datetime_event_start
            and message.from_user
            and message.from_user.username
            and config.secret_trash
        ):

            user_hash = hash(message.from_user.username + config.secret_trash)
            await message.answer(
                facts_format_text[lang].format("?")
                + facts_text[lang][0].format(user_hash),
                reply_markup=make_back_to_main_menu_keyboard(),
            )

            return

        fact_id = random.randint(1, len(facts_text[lang]) - 1)

        await message.answer(
            facts_format_text[lang].format(fact_id) + facts_text[lang][fact_id],
            reply_markup=make_back_to_main_menu_keyboard(),
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

        if message.reply_to_message and message.reply_to_message.html_text:
            user_id = message.reply_to_message.md_text.split("\n", 2)[1]
            text = message.html_text.split(maxsplit=1)[1]
        else:
            parts = message.html_text.split(maxsplit=2)

            if len(parts) < 3:
                await message.answer(
                    "Команда должна быть в формате `/ans [(u){user id} | {request id}] [text]` (u{user id} - отправить сообщение пользователю, {request id} - отправить сообщение по запросу)\nИли должна отвечать на запрос и написана в виде `/ans [text]`\nНапример, /ans u909582648 Когда долг вернёшь?\n\n или /ans 35935192 Ваше обращение не будет рассмотрено!",
                    parse_mode="Markdown",
                )
                return

            user_id = parts[1]
            text = parts[2]

        if user_id.startswith("u"):
            user_id = user_id[1:]
            await self.bot.send_message(
                user_id, f"Сообщение по одному из ваших обращений:\n\n{text}"
            )
            await message.answer(f"Ответ отправлен пользователю {user_id}: \n {text}")
            await try_delete_message(message)
            return

        try:
            request_sender = BotStorage().get_request(int(user_id))["user_id"]
            BotStorage().add_request_answer(int(user_id), text)
            await self.bot.send_message(
                request_sender, f"Ответ по вашему обращению {user_id}:\n\n{text}"
            )
            if message.reply_to_message and message.reply_to_message.html_text:
                reply_sender = (
                    (message.from_user.username or message.from_user.id)
                    if message.from_user
                    else "Аноним"
                )
                reply_parts = message.reply_to_message.html_text.rsplit("————", 1)
                reply_text = f"{reply_parts[0]}————\n\nОтвет от @{reply_sender}:\n{text}\n\n————{reply_parts[1]}"
                await self.bot.edit_message_text(
                    text=reply_text,
                    chat_id=message.reply_to_message.chat.id,
                    message_id=message.reply_to_message.message_id,
                )
                await try_delete_message(message)
            else:
                await message.answer(
                    f"Ответ отправлен пользователю {request_sender}: \n {text}"
                )
                await try_delete_message(message)
        except ValueError:
            await message.answer(f"Запроса номер {user_id} не существует")
            return
