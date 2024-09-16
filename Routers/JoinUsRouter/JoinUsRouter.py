from aiogram import Router, Bot, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import FSInputFile

from Utils.KeyboardMaker import make_keyboard, button_text_back_to_main_menu

from .JoinUsRouterTexts import *
from ..MainRouter.MainRouterTexts import button_text_work_with_us

from Utils.Utils import answer_callback, get_lang_from_state


class JoinUsRouterState(StatesGroup):
    default = State()


class JoinUsRouter(Router):
    def __init__(self, bot: Bot) -> None:
        super().__init__()

        self.bot = bot

        self.callback_query.register(
            self.enter_handler, F.data == button_text_work_with_us["en"][1]
        )
        self.callback_query.register(self.option_is_unavailable, F.data == "ju_unvbl")

        self.photo_file = FSInputFile("./Assets/WorkWithUsProfile.webp")

    async def enter_handler(self, callback: CallbackQuery, state: FSMContext) -> None:
        await state.set_state(JoinUsRouterState.default)
        await callback.answer()

        lang = await get_lang_from_state(state)

        await answer_callback(
            bot=self.bot,
            callback=callback,
            text=block_enter_text_vu[lang],
            reply_markup=make_keyboard(
                button_text_become_delegate_u[lang],
                button_text_become_volunteer_a[lang],
                button_text_back_to_main_menu[lang],
            ),
            photo=self.photo_file,
        )

    async def option_is_unavailable(
        self, callback: CallbackQuery, state: FSMContext
    ) -> None:
        lang = await get_lang_from_state(state)
        await callback.answer(option_is_temporarily_unavailable_text[lang])
