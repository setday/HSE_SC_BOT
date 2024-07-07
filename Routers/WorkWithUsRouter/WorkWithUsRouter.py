from aiogram import Router, Bot, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from Routers.DefaultTexts import get_lang_from_state
from Routers.KeyboardMaker import make_back_to_main_menu_keyboard

from .WorkWithUsRouterTexts import *
from ..MainRouter.MainRouterTexts import button_text_work_with_us

from ..Utils import answer_callback


class WorkWithUsRouterState(StatesGroup):
    default = State()


class WorkWithUsRouter(Router):
    def __init__(self, bot: Bot) -> None:
        super().__init__()

        self.bot = bot

        self.callback_query.register(
            self.enter_handler, F.data == button_text_work_with_us["en"][1]
        )

    async def enter_handler(self, callback: CallbackQuery, state: FSMContext) -> None:
        await state.set_state(WorkWithUsRouterState.default)
        await callback.answer()

        lang = await get_lang_from_state(state)

        await answer_callback(
            bot=self.bot,
            callback=callback,
            text=block_enter_text[lang],
            reply_markup=make_back_to_main_menu_keyboard(lang),
        )
