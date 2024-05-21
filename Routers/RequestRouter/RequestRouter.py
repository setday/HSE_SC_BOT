from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from Logger.BackChatUtils import send_data_to_back
from .RequestRouterTexts import *
from ..MainRouter.MainRouterTexts import button_option_request, button_option_request_alt

from Routers.DefaultTexts import send_text, sent_text, cancel_text
from Routers.KeyboardMaker import make_keyboard, make_back_keyboard


class RequestRouterState(StatesGroup):
    default = State()

class RequestRouter(Router):
    def __init__(self, bot: Bot) -> None:
        super().__init__()

        self.bot = bot

        self.callback_query.register(self.enter_handler, F.data == button_option_request)
        self.callback_query.register(self.enter_handler, F.data == button_option_request_alt)
        self.callback_query.register(self.cont_handler, F.data == button_option_another)
        self.callback_query.register(self.cont_handler, F.data == button_option_campus)
        self.callback_query.register(self.cont_handler, F.data == button_option_support[:30])
        self.callback_query.register(self.cont_handler, F.data == button_option_dormitory)
        self.callback_query.register(self.cont_handler, F.data == button_option_edu[:30])
        self.callback_query.register(self.send_handler, F.data == send_text)
        self.message.register(self.default_reqest_handler, RequestRouterState.default)

    async def enter_handler(self, callback: CallbackQuery, state: FSMContext) -> None:
        await self.bot.send_message(
            callback.from_user.id,
            block_enter_text,
            reply_markup=make_keyboard(
                button_option_edu,
                button_option_support,
                button_option_campus,
                button_option_dormitory,
                button_option_another
            )
        )
        await callback.answer()

        await state.set_state(RequestRouterState.default)

    async def cont_handler(self, callback: CallbackQuery, state: FSMContext) -> None:
        await self.bot.send_message(callback.from_user.id, block_enter_text_2)
        await callback.answer()

        await state.set_data({'request_type': callback.data})

    async def default_reqest_handler(self, message: Message, state: FSMContext) -> None:
        if not message.from_user:
            await message.answer(unknown_user)
            return

        request_text = f"Обращение от {message.from_user.first_name or ''} {message.from_user.last_name or ''} (@{message.from_user.username or ''}):\n\n{message.html_text}"
        await state.set_data({'request': request_text})

        await message.answer(
            block_default_text + "\n\n-------\n" + request_text + "\n-------",
            reply_markup=make_keyboard(
                send_text,
                cancel_text
            ),
            parse_mode="HTML"
        )

    async def send_handler(self, callback: CallbackQuery, state: FSMContext) -> None:
        data = await state.get_data()

        await send_data_to_back(self.bot, data['request'])

        await callback.answer(sent_text)

        await self.bot.send_message(callback.from_user.id, reqest_registred_text, reply_markup=make_back_keyboard())
