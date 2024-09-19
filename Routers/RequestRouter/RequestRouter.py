from datetime import datetime, timedelta

from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery, User
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import FSInputFile

from Utils.BotStorage import BotStorage
from Utils.BackChatUtils import send_request_to_back
from .RequestRouterTexts import *

from Utils.DefaultTexts import button_text_back_to_main_menu
from Utils.KeyboardMaker import make_keyboard, make_back_to_main_menu_keyboard

from ..MainRouter.MainRouterTexts import button_text_leave_request_to_sc

from Utils.Utils import answer_callback, get_lang_from_state


class RequestRouterState(StatesGroup):
    default = State()
    faculty_and_course_requested = State()

    topic_requested = State()
    faculty_requested = State()
    course_requested = State()
    campus_or_dormitory_requested = State()

    application_requested = State()
    entering_application = State()
    confirm_application = State()


class RequestRouter(Router):
    def __init__(self, bot: Bot) -> None:
        super().__init__()

        self.bot = bot

        self.callback_query.register(
            self.enter_handler, F.data == button_text_leave_request_to_sc["en"][1]
        )
        self.callback_query.register(
            self.enter_handler, F.data == button_text_back_to_topic["en"][1]
        )

        self.callback_query.register(self.show_sent_requests, F.data == "shw_appls")
        self.callback_query.register(self.print_request_n, F.data.startswith("req_"))

        self.callback_query.register(
            self.register_topic_handler, RequestRouterState.topic_requested
        )

        self.callback_query.register(
            self.ask_for_faculty, F.data == button_text_back_to_faculty["en"][1]
        )
        self.callback_query.register(
            self.ask_for_course, RequestRouterState.faculty_requested
        )

        self.message.register(
            self.application_reqest_handler_m,
            RequestRouterState.campus_or_dormitory_requested,
        )

        self.callback_query.register(
            self.application_reqest_handler_c,
            F.data == button_text_back_to_application["en"][1],
        )
        self.callback_query.register(
            self.application_reqest_handler_c, RequestRouterState.application_requested
        )
        self.callback_query.register(
            self.application_reqest_handler_c_from_cource,
            RequestRouterState.course_requested,
        )

        self.callback_query.register(
            self.send_handler, F.data == button_text_approve_application["en"][1]
        )

        self.message.register(
            self.application_applience_handler, RequestRouterState.entering_application
        )

        self.photo_file = FSInputFile("./Assets/RequestProfile.webp")

    async def reset_user(
        self,
        state: FSMContext,
        callback: CallbackQuery | None = None,
        message: Message | None = None,
    ) -> None:
        lang = await get_lang_from_state(state)

        await state.set_state(None)
        if callback:
            await callback.answer(unexpected_error_text)
            await answer_callback(
                bot=self.bot,
                callback=callback,
                text=f"{something_went_wrong_text[lang]} \n\n",
                reply_markup=make_keyboard(button_text_back_to_main_menu[lang]),
                saveMedia=False,
            )

    async def enter_handler(self, callback: CallbackQuery, state: FSMContext) -> None:
        await state.set_state(RequestRouterState.topic_requested)

        lang = await get_lang_from_state(state)

        await answer_callback(
            bot=self.bot,
            callback=callback,
            text=block_enter_text[lang],
            reply_markup=make_keyboard(
                *button_text_topics[lang],
            ),
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

        await callback.answer()

    async def register_topic_handler(
        self, callback: CallbackQuery, state: FSMContext
    ) -> None:
        if callback.data is None:
            await callback.answer(unexpected_error_text)
            return
        if callback.data not in button_text_topics_ids.keys():
            await self.reset_user(state, callback=callback)
            return

        await state.update_data(request_type=button_text_topics_ids[callback.data])

        if callback.data == "ct_cmp_or_drm_prb":
            await self.ask_for_campus_or_dormitory(callback, state)
        elif callback.data == "ct_edu_prb" or callback.data == "ct_app_com":
            await self.ask_for_faculty(callback, state)
        else:
            await state.set_state(RequestRouterState.application_requested)
            await self.application_reqest_handler_c(callback, state)

    async def show_sent_requests(
        self, callback: CallbackQuery, state: FSMContext
    ) -> None:
        await callback.answer()

        lang = await get_lang_from_state(state)

        data = await state.get_data()
        request_queue = data.get("request_queue", [])

        answer_text = no_sent_requests_text[lang]
        if len(request_queue):
            answer_text = sent_requests_text[lang].format(
                "".join(
                    [
                        sent_request_text[lang].format(
                            request["number"],
                            str(request["date"])[:-7],
                            request["topic"],
                        )
                        for request in request_queue[-3:]
                    ]
                )
            )

        await answer_callback(
            bot=self.bot,
            callback=callback,
            text=answer_text,
            reply_markup=make_keyboard(
                *[
                    (str(req["number"]), f"req_{i}")
                    for i, req in enumerate(request_queue[-3:])
                ],
                button_text_back_to_main_menu[lang],
            ),
        )

    async def print_request_n(self, callback: CallbackQuery, state: FSMContext) -> None:
        if not callback.data:
            await self.reset_user(state, callback=callback)
            return

        lang = await get_lang_from_state(state)

        data = await state.get_data()
        request_queue = data.get("request_queue", [])

        request = request_queue[int(callback.data.split("_")[1])]

        if not request:
            await self.reset_user(state, callback=callback)
            return

        await callback.answer()

        await answer_callback(
            bot=self.bot,
            callback=callback,
            text=request["request"],
            reply_markup=make_keyboard(
                button_your_requests_text[lang],
            ),
        )

    async def ask_for_campus_or_dormitory(
        self, callback: CallbackQuery, state: FSMContext
    ) -> None:
        await state.set_state(RequestRouterState.campus_or_dormitory_requested)

        await callback.answer()

        lang = await get_lang_from_state(state)

        await answer_callback(
            bot=self.bot,
            callback=callback,
            text=write_campus_or_dormitory_text[lang],
            reply_markup=make_keyboard(button_text_back_to_topic[lang]),
        )

    async def ask_for_faculty(self, callback: CallbackQuery, state: FSMContext) -> None:
        await state.set_state(RequestRouterState.faculty_requested)

        await callback.answer()

        lang = await get_lang_from_state(state)

        await answer_callback(
            bot=self.bot,
            callback=callback,
            text=choose_faculty_text[lang],
            reply_markup=make_keyboard(*button_text_faculties[lang]),
        )

    async def ask_for_course(self, callback: CallbackQuery, state: FSMContext) -> None:
        await state.set_state(RequestRouterState.course_requested)

        if callback.data is None:
            await callback.answer(unexpected_error_text)
            return
        if callback.data not in button_text_faculties_ids.keys():
            await self.reset_user(state, callback=callback)
            return

        await callback.answer()
        await state.update_data(faculty=button_text_faculties_ids[callback.data])

        lang = await get_lang_from_state(state)

        await answer_callback(
            bot=self.bot,
            callback=callback,
            text=choose_course_text[lang],
            reply_markup=make_keyboard(*button_text_courses[lang]),
        )

    ###
    # End state: application_requested
    ###

    async def application_reqest_handler_m(
        self, message: Message, state: FSMContext
    ) -> None:
        if not message.from_user:
            await message.answer(
                unknown_user_text, reply_markup=make_back_to_main_menu_keyboard()
            )
            return

        await state.set_state(RequestRouterState.entering_application)

        await state.update_data(campus_or_dormitory=message.html_text)

        lang = await get_lang_from_state(state)

        await message.answer(
            request_full_descr_text[lang],
            reply_markup=make_keyboard(button_text_back_to_topic[lang]),
            parse_mode="HTML",
        )

    async def application_reqest_handler_c(
        self, callback: CallbackQuery, state: FSMContext
    ) -> None:
        await state.set_state(RequestRouterState.entering_application)

        await callback.answer()

        lang = await get_lang_from_state(state)

        await answer_callback(
            bot=self.bot,
            callback=callback,
            text=request_full_descr_text[lang],
            reply_markup=make_keyboard(button_text_back_to_topic[lang]),
            parse_mode="HTML",
        )

    async def application_reqest_handler_c_from_cource(
        self, callback: CallbackQuery, state: FSMContext
    ) -> None:
        if not callback.data or callback.data not in button_text_courses_ids.keys():
            await self.reset_user(state, callback=callback)
            return

        await state.update_data(course=button_text_courses_ids[callback.data])

        await self.application_reqest_handler_c(callback, state)

    def assemble_reqest(self, data: dict, user: User, lang: str = "ru") -> str:
        second_row = ""
        if data.get("campus_or_dormitory"):
            second_row = campus_or_dormitory_text[lang] + data["campus_or_dormitory"]
        elif data.get("faculty"):
            second_row = faculty[lang] + button_text_faculties[lang][data["faculty"]][0]

        third_row = ""
        if data.get("course"):
            third_row = course[lang] + button_text_courses[lang][data["course"]][0]

        return application_sent_text[lang].format(
            user_name=user.full_name,
            user_nick=user.username or "",
            user_id=user.id,
            topic=button_text_topics[lang][data.get("request_type", 3)][0],
            second_row=second_row,
            third_row=third_row,
            text=data.get("request_text", ""),
        )

    async def application_applience_handler(
        self, message: Message, state: FSMContext
    ) -> None:
        if not message.from_user:
            await message.answer(unknown_user_text)
            return

        await state.set_state(RequestRouterState.confirm_application)

        data = await state.get_data()
        data.update(request_text=message.html_text)

        request_text_to_send = self.assemble_reqest(data, message.from_user)
        await state.update_data(request_to_send=request_text_to_send)

        lang = await get_lang_from_state(state)

        request_text = self.assemble_reqest(data, message.from_user, lang)
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

        topic = "Cooperation"
        if data["request_type"]:
            topic = button_text_topics[lang][data["request_type"]][0]

        request_queue.append(
            {
                "number": request_id,
                "date": datetime.now(),
                "request": data["request"],
                "topic": topic,
            }
        )
        BotStorage().add_request(
            {
                "request_id": request_id,
                "date": datetime.now(),
                "user_id": callback.from_user.id,
                "topic": topic,
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
