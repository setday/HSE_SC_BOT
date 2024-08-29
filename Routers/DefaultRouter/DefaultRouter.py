from aiogram import Router, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from ..Filters import SuperChatFilter

from keysLoader import get_vote_id, get_back_id

from Routers.KeyboardMaker import make_back_to_main_menu_keyboard

from .DefaultRouterTexts import unknown_action_text

from ..Utils import get_lang_from_state


class DefaultRouter(Router):
    def __init__(self, bot: Bot) -> None:
        super().__init__()

        self.bot = bot

        self.message.register(self.default_handler, SuperChatFilter(False))
        self.callback_query.register(self.default_callback_handler)

    async def default_handler(self, message: Message, state: FSMContext) -> None:
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
