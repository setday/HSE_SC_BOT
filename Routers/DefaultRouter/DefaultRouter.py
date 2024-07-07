from aiogram import Router, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from Routers.DefaultTexts import get_lang_from_state
from Routers.KeyboardMaker import make_back_to_main_menu_keyboard

from .DefaultRouterTexts import unknown_action_text


class DefaultRouter(Router):
    def __init__(self, bot: Bot) -> None:
        super().__init__()

        self.bot = bot

        self.message.register(self.default_handler)
        self.callback_query.register(self.default_callback_handler)

    async def default_handler(self, message: Message, state: FSMContext) -> None:
        print("Unhandeled message:", message.text)
        lang = await get_lang_from_state(state)
        await message.answer(
            unknown_action_text[lang], reply_markup=make_back_to_main_menu_keyboard()
        )

    async def default_callback_handler(
        self, callback: CallbackQuery, state: FSMContext
    ) -> None:
        print("Unhandeled callback:", callback.data)
        lang = await get_lang_from_state(state)
        await callback.answer(unknown_action_text[lang])
