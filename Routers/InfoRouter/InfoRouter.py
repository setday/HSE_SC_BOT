from aiogram import Router, Bot, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from Routers.DefaultTexts import back_to_menu_text
from Routers.KeyboardMaker import make_keyboard

from .InfoRouterTexts import *
from ..MainRouter.MainRouterTexts import button_option_info

from ..Utils import answer_callback

class InfoRouterState(StatesGroup):
    default = State()

class InfoRouter(Router):
    def __init__(self, bot: Bot) -> None:
        super().__init__()

        self.bot = bot

        self.callback_query.register(self.enter_handler, F.data == button_option_info)
        self.callback_query.register(self.links_hndler, InfoRouterState.default, F.data == button_option_links)
        self.callback_query.register(self.members_hndler, InfoRouterState.default, F.data == button_option_members)

    async def enter_handler(self, callback: CallbackQuery, state: FSMContext) -> None:
        await state.set_state(InfoRouterState.default)

        await answer_callback(
            bot=self.bot,
            callback=callback,
            text=block_enter_text,
            reply_markup=make_keyboard(
                button_option_members,
                button_option_links,
                back_to_menu_text
            ),
        )

        await callback.answer()

    async def links_hndler(self, callback: CallbackQuery, state: FSMContext) -> None:
        await answer_callback(
            bot=self.bot,
            callback=callback,
            text=links_text,
            reply_markup=make_keyboard(
                button_option_members,
                back_to_menu_text
            )
        )
        await callback.answer()

    async def members_hndler(self, callback: CallbackQuery, state: FSMContext) -> None:
        await answer_callback(
            bot=self.bot,
            callback=callback,
            text=members_text,
            reply_markup=make_keyboard(
                button_option_links,
                back_to_menu_text
            )
        )
        await callback.answer()
