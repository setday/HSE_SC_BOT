from docx import Document
import re

from aiogram import Router, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from keysLoader import get_vote_id, get_back_id

from Routers.DefaultTexts import get_lang_from_state
from Routers.KeyboardMaker import make_back_to_main_menu_keyboard

from .DefaultRouterTexts import unknown_action_text


def get_dead_list(file):
    res = []

    doc = Document(file)
    for para in doc.paragraphs:
        re_res = re.findall(r"рименить в отношении студентов.*меру дисциплинарного взыскания", para.text)
        for r in re_res:
            res.append(r[31:-31])

    return res


class DefaultRouter(Router):
    def __init__(self, bot: Bot) -> None:
        super().__init__()

        self.bot = bot

        self.message.register(self.default_handler)
        self.callback_query.register(self.default_callback_handler)

    async def create_bc_poll(self, message: Message) -> None:
        if message.document is None or message.document.mime_type != "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            return
        
        file = await self.bot.download(message.document.file_id)
        if file is None:
            return
        
        dead_list = get_dead_list(file)
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

    async def default_handler(self, message: Message, state: FSMContext) -> None:
        if message.chat.id == get_vote_id() and message.document and message.document.mime_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            await self.create_bc_poll(message)
            return
        
        if message.chat.id == get_vote_id() or message.chat.id == get_back_id():
            return

        print("Unhandeled message:", message.text, message.document, message.media_group_id)
        
        lang = await get_lang_from_state(state)
        await message.answer(
            unknown_action_text[lang], reply_markup=make_back_to_main_menu_keyboard()
        )

    async def default_callback_handler(
        self, callback: CallbackQuery, state: FSMContext
    ) -> None:
        if not callback.message or callback.message.chat.id == get_vote_id() or callback.message.chat.id == get_back_id():
            return

        print("Unhandeled callback:", callback.data)
        lang = await get_lang_from_state(state)
        await callback.answer(unknown_action_text[lang])
