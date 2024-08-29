from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from Logger.BackChatUtils import send_data_to_back
from .RequestRouterTexts import *

from Routers.DefaultTexts import button_text_back_to_main_menu
from Routers.KeyboardMaker import make_keyboard, make_back_to_main_menu_keyboard

from ..MainRouter.MainRouterTexts import button_text_leave_request_to_sc

from ..Utils import answer_callback, get_lang_from_state


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
            self.application_reqest_handler_m, RequestRouterState.campus_or_dormitory_requested
        )

        self.callback_query.register(
            self.application_reqest_handler_c,
            F.data == button_text_back_to_application["en"][1],
        )
        self.callback_query.register(
            self.application_reqest_handler_c, RequestRouterState.application_requested
        )
        self.callback_query.register(
            self.application_reqest_handler_c_from_cource, RequestRouterState.course_requested
        )

        self.callback_query.register(
            self.send_handler, F.data == button_text_approve_application["en"][1]
        )

        self.message.register(
            self.application_applience_handler, RequestRouterState.entering_application
        )

    async def reset_user(self, state: FSMContext, callback: CallbackQuery | None = None, message: Message | None = None) -> None:
        lang = await get_lang_from_state(state)

        await state.set_state(None)
        if callback:
            await callback.answer(unexpected_error_text)
            await answer_callback(
                bot=self.bot,
                callback=callback,
                text=f'{something_went_wrong_text[lang]} \n\n',
                reply_markup=make_keyboard(button_text_back_to_main_menu[lang]),
                parse_mode="HTML",
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
        )

        await state.update_data(faculty=None, course=None, campus_or_dormitory=None, request_type=None)

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

        if callback.data == "in_dev":
            await callback.answer("This feature is in development")
            return
        elif callback.data == "ct_cmp_or_drm_prb":
            await self.ask_for_campus_or_dormitory(callback, state)
        elif callback.data == "ct_edu_prb" or callback.data == "ct_app_com":
            await self.ask_for_faculty(callback, state)
        else:
            await state.set_state(RequestRouterState.application_requested)
            await self.application_reqest_handler_c(callback, state)

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
            await message.answer(unknown_user_text, reply_markup=make_back_to_main_menu_keyboard())
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

    async def application_applience_handler(
        self, message: Message, state: FSMContext
    ) -> None:
        if not message.from_user:
            await message.answer(unknown_user_text)
            return

        await state.set_state(RequestRouterState.confirm_application)

        data = await state.get_data()

        lang = await get_lang_from_state(state)

        second_row_ru = ""
        if data.get("campus_or_dormitory", None):
            second_row_ru = (
                campus_or_dormitory_text["ru"] + data["campus_or_dormitory"]
            )
        elif data.get("faculty", None):
            second_row_ru = (
                faculty["ru"] + button_text_faculties["ru"][data["faculty"]][0]
            )
        else:
            second_row_ru = ""
        third_row_ru = (
            course["ru"] +
            button_text_courses["ru"][data["course"]][0] if data.get("course", None) else ""
        )

        second_row_native = ""
        if data.get("campus_or_dormitory", None):
            second_row_native = (
                campus_or_dormitory_text[lang] + data["campus_or_dormitory"]
            )
        elif data.get("faculty", None):
            second_row_native = (
                faculty[lang] + button_text_faculties[lang][data["faculty"]][0]
            )
        else:
            second_row_native = ""
        third_row_native = (
            course[lang] +
            button_text_courses["ru"][data["course"]][0] if data.get("course", None) else ""
        )

        request_text_to_send = application_sent_text.format(
            f"{message.from_user.first_name or ''} {message.from_user.last_name or ''}",
            message.from_user.username or "",
            button_text_topics["ru"][data.get("request_type", 3)][0],
            second_row_ru,
            third_row_ru,
            message.html_text,
        )
        await state.update_data(request=request_text_to_send)

        request_text = confirm_application_text[lang].format(
            f"{message.from_user.first_name or ''} {message.from_user.last_name or ''}",
            message.from_user.username or "",
            button_text_topics[lang][data.get("request_type", 3)][0],
            second_row_native,
            third_row_native,
            message.html_text,
        )

        await message.answer(
            request_text,
            reply_markup=make_keyboard(
                button_text_approve_application[lang],
                button_text_back_to_application[lang],
            ),
            parse_mode="HTML",
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
