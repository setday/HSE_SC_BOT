from datetime import datetime, timedelta

from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery, User
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import FSInputFile

from Utils.BotStorage import BotStorage
from Utils.KeyboardMaker import make_keyboard, make_back_to_main_menu_keyboard

from Utils.BackChatUtils import send_request_to_back
from .PartnershipRouterTexts import *
from ..MainRouter.MainRouterTexts import button_text_partnership

from Utils.Utils import answer_callback, get_lang_from_state


class PartnershipRouterState(StatesGroup):
    default = State()
    entering_application = State()
    confirm_application = State()


class PartnershipRouter(Router):
    def __init__(self, bot: Bot) -> None:
        super().__init__()

        self.bot = bot

        self.callback_query.register(
            self.enter_handler, F.data == button_text_partnership["en"][1]
        )
        self.callback_query.register(
            self.enter_handler, F.data == button_text_back_to_application["en"][1]
        )

        self.message.register(
            self.application_applience_handler,
            PartnershipRouterState.entering_application,
        )
        self.callback_query.register(
            self.send_handler, F.data == button_text_approve_application["en"][1]
        )

        self.photo_file = FSInputFile("./Assets/PartnershipProfile.webp")

    async def enter_handler(self, callback: CallbackQuery, state: FSMContext) -> None:
        await state.set_state(PartnershipRouterState.entering_application)

        await callback.answer()

        lang = await get_lang_from_state(state)

        await answer_callback(
            bot=self.bot,
            callback=callback,
            text=block_enter_text[lang],
            reply_markup=make_back_to_main_menu_keyboard(lang),
            parse_mode="HTML",
            photo=self.photo_file,
        )

        await state.update_data(
            faculty=None,
            course=None,
            campus_or_dormitory=None,
            request_type=None,
            request_to_send=None,
            request=None,
        )

    def combine_reqest(self, text: str, user: User, lang: str = "ru") -> str:
        # second_row = ""
        # if "campus_or_dormitory" in data:
        #     second_row = campus_or_dormitory_text[lang] + data["campus_or_dormitory"]
        # elif "faculty" in data:
        #     second_row = faculty[lang] + button_text_faculties[lang][data["faculty"]][0]

        # third_row = ""
        # if "course" in data:
        #     third_row = course[lang] + button_text_courses[lang][data["course"]][0]

        return application_sent_text[lang].format(
            user_name=user.full_name,
            user_nick=user.username or "",
            user_id=user.id,
            # topic=button_text_topics[lang][data.get("request_type", 3)][0],
            # second_row=second_row,
            # third_row=third_row,
            text=text,
        )

    async def application_applience_handler(
        self, message: Message, state: FSMContext
    ) -> None:
        if not message.from_user:
            await message.answer(unknown_user_text)
            return

        await state.set_state(PartnershipRouterState.confirm_application)

        request_text_to_send = self.combine_reqest(message.html_text, message.from_user)
        await state.update_data(request_to_send=request_text_to_send)

        lang = await get_lang_from_state(state)
        request_text = self.combine_reqest(message.html_text, message.from_user, lang)
        await state.update_data(request=request_text)

        await message.answer(
            confirm_application_text[lang].format(request_text),
            reply_markup=make_keyboard(
                button_text_approve_application[lang],
                button_text_back_to_application[lang],
            ),
            parse_mode="HTML",
        )

    async def send_handler(self, callback: CallbackQuery, state: FSMContext) -> None:
        lang = await get_lang_from_state(state)

        data = await state.get_data()
        request_queue = data.get("request_queue", [])

        if len(request_queue) > 0 and request_queue[-1][
            "date"
        ] > datetime.now() + timedelta(seconds=-6):
            await callback.answer(wait_a_little_text[lang])
            return

        request_id = await send_request_to_back(self.bot, data["request"])
        await callback.answer()

        request_queue.append(
            {
                "number": request_id,
                "date": datetime.now(),
                "request": data["request"],
                "topic": "Cooperation",
            }
        )
        BotStorage().add_request(
            {
                "request_id": request_id,
                "date": datetime.now(),
                "user_id": callback.from_user.id,
                "topic": "Cooperation",
                "request": data["request"],
            },
            request_id,
        )
        await state.update_data(request_queue=request_queue)

        await answer_callback(
            bot=self.bot,
            callback=callback,
            text=reqest_registred_text[lang].format(request_id),
            reply_markup=make_back_to_main_menu_keyboard(lang),
        )
        await state.update_data(request=None)
