from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart
from aiogram.fsm.state import StatesGroup, State

from ..Filters import SuperChatFilter

from Routers.DefaultTexts import button_text_back_to_main_menu
from Routers.KeyboardMaker import make_keyboard

from .MainRouterTexts import *

from ..Utils import answer_callback, get_lang_from_state


class MainRouterState(StatesGroup):
    language_selection = State()
    main_menu = State()
    default = State()


class MainRouter(Router):
    def __init__(self, bot: Bot) -> None:
        super().__init__()

        self.bot = bot

        self.message.register(self.enter_handler, CommandStart(), SuperChatFilter(False))
        self.callback_query.register(
            self.language_selection_handler,
            F.data == button_text_change_language["en"][1],
        )
        self.callback_query.register(
            self.language_selected_handler, MainRouterState.language_selection
        )
        self.callback_query.register(
            self.main_menu_handler, F.data == button_text_back_to_main_menu["en"][1]
        )

    # Enter handlers
    async def enter_handler(self, message: Message, state: FSMContext) -> None:
        status = await state.get_state()
        if status:
            await message.delete()
            return

        await state.set_state(MainRouterState.language_selection)

        await message.answer(
            block_enter_text,
            reply_markup=make_keyboard(
                button_text_lang["ru"],
                button_text_lang["en"],
            ),
        )

    async def language_selection_handler(
        self, callback: CallbackQuery, state: FSMContext
    ) -> None:
        await state.set_state(MainRouterState.language_selection)

        await callback.answer()

        await answer_callback(
            bot=self.bot,
            callback=callback,
            text=block_enter_text,
            reply_markup=make_keyboard(
                button_text_lang["ru"],
                button_text_lang["en"],
            ),
        )

    async def language_selected_handler(
        self, callback: CallbackQuery, state: FSMContext
    ) -> None:
        await state.set_state(MainRouterState.default)

        lang = callback.data if callback.data in ["ru", "en"] else "ru"
        await state.update_data(language=lang)

        await self.main_menu_handler(callback, state)

    async def main_menu_handler(
        self, callback: CallbackQuery, state: FSMContext
    ) -> None:
        await state.set_state(MainRouterState.main_menu)
        
        await callback.answer()

        lang = await get_lang_from_state(state)

        await answer_callback(
            bot=self.bot,
            callback=callback,
            text=navigation_text[lang],
            reply_markup=make_keyboard(
                button_text_leave_request_to_sc[lang],
                button_text_work_with_us[lang],
                button_text_info_about_sc[lang],
                button_text_change_language[lang],
                button_text_partnership[lang],
            ),
        )
