from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from Logger.BackChatUtils import send_data_to_back
from .RequestRouterTexts import *
from ..MainRouter.MainRouterTexts import button_option_request, button_option_request_alt

from Routers.DefaultTexts import send_text, sent_text, cancel_text
from Routers.KeyboardMaker import make_keyboard, make_back_keyboard

from ..Utils import answer_callback


class RequestRouterState(StatesGroup):
    default = State()
    faculty_and_course_requested = State()

class RequestRouter(Router):
    def __init__(self, bot: Bot) -> None:
        super().__init__()

        self.bot = bot

        self.callback_query.register(self.enter_handler, F.data == button_option_request)
        self.callback_query.register(self.enter_handler, F.data == button_option_request_alt)
        self.callback_query.register(self.request_type_handler, F.data == button_option_another)
        self.callback_query.register(self.request_type_handler, F.data == button_option_campus)
        self.callback_query.register(self.request_type_handler, F.data == button_option_dormitory)
        self.callback_query.register(self.request_faculty_and_course_handler, F.data == button_option_support[:30])
        self.callback_query.register(self.request_faculty_and_course_handler, F.data == button_option_edu[:30])
        self.message.register(self.request_type_msg_handler, RequestRouterState.faculty_and_course_requested)
        self.callback_query.register(self.send_handler, F.data == send_text)
        self.message.register(self.default_reqest_handler, RequestRouterState.default)

    async def enter_handler(self, callback: CallbackQuery, state: FSMContext) -> None:
        await answer_callback(
            bot=self.bot,
            callback=callback,
            text=block_enter_text,
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

    async def request_type_handler(self, callback: CallbackQuery, state: FSMContext) -> None:
        await answer_callback(
            bot=self.bot,
            callback=callback,
            text=detailed_text,
            reply_markup=make_back_keyboard()
        )
        await callback.answer()

        await state.set_data({"request_type": callback.data})

    async def request_type_msg_handler(self, message: Message, state: FSMContext) -> None:
        await message.answer(detailed_text)

        await state.update_data({"faculty_and_course": message.text})
        await state.set_state(RequestRouterState.default)

    async def request_faculty_and_course_handler(self, callback: CallbackQuery, state: FSMContext) -> None:
        await answer_callback(
            bot=self.bot,
            callback=callback,
            text=faculty_question_text,
            reply_markup=make_back_keyboard()
        )
        await callback.answer()

        await state.set_data({"request_type": callback.data})
        await state.set_state(RequestRouterState.faculty_and_course_requested)

    async def default_reqest_handler(self, message: Message, state: FSMContext) -> None:
        if not message.from_user:
            await message.answer(unknown_user)
            return
        
        data = await state.get_data()

        request_text = f"Обращение от {message.from_user.first_name or ''} {message.from_user.last_name or ''} (@{message.from_user.username or ''}):\n\n"
        request_text += f"Тема: {recover_option_text(data['request_type'])}\n"
        request_text += f"Факультет и курс: {data['faculty_and_course']}\n\n" if "faculty_and_course" in data else "\n"
        request_text += message.html_text
        await state.set_data({"request": request_text})

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

        number = await send_data_to_back(self.bot, data["request"])

        await callback.answer(sent_text)

        await answer_callback(
            bot=self.bot,
            callback=callback,
            text=f"Номер обращения - {number}\n\n{reqest_registred_text}",
            reply_markup=make_back_keyboard()
        )
        await state.set_data({})
