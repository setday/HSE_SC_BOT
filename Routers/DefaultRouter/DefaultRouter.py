from datetime import datetime
import pytz

from aiogram import Router, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from Utils.Filters import SuperChatFilter

from keysLoader import get_vote_id, get_back_id

from Utils.KeyboardMaker import make_back_to_main_menu_keyboard

from .DefaultRouterTexts import unknown_action_text, message_to_old_text

from Utils.Utils import get_lang_from_state


class DefaultRouter(Router):
    def __init__(self, bot: Bot) -> None:
        super().__init__()

        self.bot = bot

        self.message.register(self.default_handler, SuperChatFilter(False))
        self.message.register(self.s_default_handler, SuperChatFilter(True))
        self.callback_query.register(self.default_callback_handler)

    async def default_handler(self, message: Message, state: FSMContext) -> None:
        print(
            "Unhandeled message:",
            message.text,
            " | DOC -> | ",
            message.document,
            " | MIM -> | ",
            message.document.mime_type if message.document else None,
            " | MID -> | ",
            message.media_group_id,
            " | CID -> | ",
            message.chat.id,
        )

        lang = await get_lang_from_state(state)
        await message.answer(
            unknown_action_text[lang],
            reply_markup=make_back_to_main_menu_keyboard(),
        )

    async def s_default_handler(self, message: Message, state: FSMContext) -> None:
        print(
            "Unhandeled message:",
            message.text,
            " | DOC -> | ",
            message.document,
            " | MIM -> | ",
            message.document.mime_type if message.document else None,
            " | MID -> | ",
            message.media_group_id,
            " | CID -> | ",
            message.chat.id,
        )

    async def default_callback_handler(
        self, callback: CallbackQuery, state: FSMContext
    ) -> None:
        if (
            not callback.message
            or callback.message.chat.id == get_vote_id()
            or callback.message.chat.id == get_back_id()
        ):
            return

        print("Unhandeled callback:", callback.data)
        lang = await get_lang_from_state(state)

        sent_date = callback.message.date
        if isinstance(sent_date, int):
            sent_date = datetime.fromtimestamp(sent_date, pytz.UTC)
        if sent_date < datetime(year=2024, month=8, day=1, tzinfo=pytz.UTC):
            await callback.answer(message_to_old_text[lang])
        else:
            await callback.answer(unknown_action_text[lang])
