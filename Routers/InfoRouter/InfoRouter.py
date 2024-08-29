from aiogram import Router, Bot, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from Routers.KeyboardMaker import make_keyboard, button_text_back_to_main_menu

from .InfoRouterTexts import *
from ..MainRouter.MainRouterTexts import button_text_info_about_sc

from ..Utils import answer_callback, get_lang_from_state


class InfoRouterState(StatesGroup):
    default = State()


class InfoRouter(Router):
    def __init__(self, bot: Bot) -> None:
        super().__init__()

        self.bot = bot

        self.callback_query.register(
            self.enter_handler, F.data == button_text_info_about_sc["en"][1]
        )
        self.callback_query.register(
            self.links_hndler, F.data == button_text_links["en"][1]
        )
        self.callback_query.register(
            self.members_hndler,
            F.data == button_text_member_list["en"][1],
        )

    async def enter_handler(self, callback: CallbackQuery, state: FSMContext) -> None:
        await state.set_state(InfoRouterState.default)

        lang = await get_lang_from_state(state)

        await answer_callback(
            bot=self.bot,
            callback=callback,
            text=block_enter_text[lang],
            reply_markup=make_keyboard(
                button_text_member_list[lang], button_text_links[lang], button_text_back_to_main_menu[lang]
            ),
        )

        await callback.answer()

    async def links_hndler(self, callback: CallbackQuery, state: FSMContext) -> None:
        await callback.answer()

        lang = await get_lang_from_state(state)

        await answer_callback(
            bot=self.bot,
            callback=callback,
            text=links_text[lang],
            reply_markup=make_keyboard(button_text_member_list[lang], button_text_back_to_main_menu[lang]),
        )

    async def members_hndler(self, callback: CallbackQuery, state: FSMContext) -> None:
        await callback.answer()

        lang = await get_lang_from_state(state)
        
        await answer_callback(
            bot=self.bot,
            callback=callback,
            text=members_text,
            reply_markup=make_keyboard(button_text_links[lang], button_text_back_to_main_menu[lang]),
            disable_web_page_preview=True,
        )
