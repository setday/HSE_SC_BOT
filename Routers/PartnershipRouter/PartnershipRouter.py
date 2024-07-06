from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from Routers.DefaultTexts import get_lang_from_state
from Routers.KeyboardMaker import make_keyboard, make_back_to_main_menu_keyboard

from Logger.BackChatUtils import send_data_to_back
from .PartnershipRouterTexts import *
from ..MainRouter.MainRouterTexts import button_text_partnership

from ..Utils import answer_callback

class PartnershipRouterState(StatesGroup):
    default = State()
    entering_application = State()
    confirm_application = State()

class PartnershipRouter(Router):
    def __init__(self, bot: Bot) -> None:
        super().__init__()

        self.bot = bot

        self.callback_query.register(self.enter_handler, F.data == button_text_partnership["en"][1])
        self.callback_query.register(self.enter_handler, F.data == button_text_back_to_application["en"][1])

        self.message.register(self.application_applience_handler, PartnershipRouterState.entering_application)
        self.callback_query.register(self.send_handler, F.data == button_text_approve_application["en"][1])

    async def enter_handler(self, callback: CallbackQuery, state: FSMContext) -> None:
        await state.set_state(PartnershipRouterState.entering_application)

        await callback.answer()

        lang = await get_lang_from_state(state)

        await answer_callback(
            bot=self.bot,
            callback=callback,
            text=block_enter_text[lang],
            reply_markup=make_back_to_main_menu_keyboard(lang),
            parse_mode="HTML"
        )

    async def application_applience_handler(self, message: Message, state: FSMContext) -> None:
        if not message.from_user:
            await message.answer(unknown_user_text)
            return
        
        await state.set_state(PartnershipRouterState.confirm_application)
        
        request_text_to_send = application_sent_text.format(
            f"{message.from_user.first_name or ''} {message.from_user.last_name or ''}",
            message.from_user.username or '',
            message.html_text
        )
        await state.update_data(request=request_text_to_send)

        lang = await get_lang_from_state(state)
        request_text = confirm_application_text[lang].format(
            f"{message.from_user.first_name or ''} {message.from_user.last_name or ''}",
            message.from_user.username or '',
            message.html_text
        )

        await message.answer(
            request_text,
            reply_markup=make_keyboard(
                button_text_approve_application[lang],
                button_text_back_to_application[lang],
            ),
            parse_mode="HTML"
        )

    async def send_handler(self, callback: CallbackQuery, state: FSMContext) -> None:
        data = await state.get_data()

        lang = await get_lang_from_state(state)
        number = await send_data_to_back(self.bot, data["request"])
        await callback.answer()

        await answer_callback(
            bot=self.bot,
            callback=callback,
            text=reqest_registred_text[lang].format(number),
            reply_markup=make_back_to_main_menu_keyboard(lang),
        )
        await state.update_data(request=None)
