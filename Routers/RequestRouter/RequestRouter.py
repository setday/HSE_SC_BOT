from datetime import datetime, timedelta

from aiogram import Bot, F
from aiogram.types import Message, CallbackQuery, User
from aiogram.fsm.context import FSMContext

from lib.base.AutoNode import AutoNode
from lib.base.AutoRouter import AutoRouter, ExtraAutoNodes
from lib.base.ExtraAutoNodes import MappingCallbackAutoNode

from Utils.BotStorage import BotStorage
from Utils.BackChatUtils import send_request_to_back
from .RequestRouterTexts import *

from Utils.DefaultTexts import button_text_back_to_main_menu
from Utils.KeyboardMaker import make_keyboard


from Utils.Utils import answer_callback, get_lang_from_state


class SenderAutoNode(AutoNode):
    async def callback_handler(
        self, callback: CallbackQuery, state: FSMContext
    ) -> None:
        data = await state.get_data()
        request_queue = data.get("request_queue", [])

        lang = await get_lang_from_state(state)

        if len(request_queue) > 0 and request_queue[-1][
            "date"
        ] > datetime.now() + timedelta(seconds=-6):
            await callback.answer(wait_a_little_text[lang])
            return

        request_id = await send_request_to_back(self.bot, data["request_to_send"])

        user = callback.from_user
        topic = "Cooperation"
        if data["topic"]:
            topic_id = button_text_topics_ids[data["topic"]]
            topic = topic_button_textes[topic_id][0][lang]

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
                "user_id": user.id,
                "topic": topic,
                "request": data["request"],
            },
            request_id,
        )
        await state.update_data(request_queue=request_queue)
        await state.update_data(request_id=request_id)

        await super().callback_handler(callback, state)
        
        await state.update_data(request=None)


class RequestRouter(AutoRouter):
    def __init__(self, bot: Bot) -> None:
        super().__init__(bot)

        self.create_node("leave_request_entry", block_enter_text, "./Assets/RequestProfile.webp")
        lrcd = self.create_node("leave_request_choose_dormitory", write_campus_or_dormitory_text)
        lrcf = self.create_node("leave_request_choose_faculty", choose_faculty_text)
        self.create_node("leave_request_choose_course", choose_course_text)
        lrea = self.create_node("leave_request_enter_application", request_full_descr_text)
        self.create_node("leave_request_review", confirm_application_text, node_trigger_callback=self.review_entry_func)
        self.add_node(SenderAutoNode(bot, self, "leave_request_sent", reqest_registred_text))

        self.add_node(MappingCallbackAutoNode(bot, self, "leave_request_entry_mapping", {
            "leave_request_entry_mapping_dr:0:ct_app_com": lrcf,
            "leave_request_entry_mapping_dr:0:ct_cmp_or_drm_prb": lrcd,
            "leave_request_entry_mapping_dr:0:ct_edu_prb": lrcf,
            "leave_request_entry_mapping_dr:0:ct_another_prb": lrea,
        }))

        self.convert_to_entry_node("leave_request_entry")

        self.add_selector_edge("leave_request_entry", "leave_request_entry_mapping", topic_button_textes, state_destination="topic")
        self.add_button_edge("leave_request_entry", "leave_request_show_applications", button_your_requests_text, is_next_node_local=False)

        self.add_message_edge("leave_request_choose_dormitory", "leave_request_enter_application", state_destination="campus_or_dormitory")
        self.add_button_edge("leave_request_choose_dormitory", "leave_request_entry", button_text_back_to_topic)

        self.add_selector_edge("leave_request_choose_faculty", "leave_request_choose_course", faculty_button_textes, state_destination="faculty")
        self.add_button_edge("leave_request_choose_faculty", "leave_request_entry", button_text_back_to_topic)
        self.add_selector_edge("leave_request_choose_course", "leave_request_enter_application", course_button_textes, state_destination="course")
        self.add_button_edge("leave_request_choose_course", "leave_request_choose_faculty", button_text_back_to_faculty)

        self.add_message_edge("leave_request_enter_application", "leave_request_review")
        self.add_button_edge("leave_request_enter_application", "leave_request_entry", button_text_back_to_topic)

        self.add_button_edge("leave_request_review", "leave_request_sent", button_text_approve_application)
        self.add_button_edge("leave_request_review", "leave_request_entry", button_text_back_to_application)

        self.add_button_edge("leave_request_entry", ExtraAutoNodes.HOME_NODE)
        self.add_button_edge("leave_request_sent", ExtraAutoNodes.HOME_NODE)

        # TODO: Remove old approach

        self.callback_query.register(self.show_sent_requests, F.data == "leave_request_show_applications")
        self.callback_query.register(self.print_request_n, F.data.startswith("req_"))


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
                (button_your_requests_text[lang], "leave_request_show_applications"),
            ),
        )

    async def assemble_request(self, data: dict, user: User | None, lang: str = "ru") -> str:
        topic_id_name = data.get("topic", "ct_another_prb")
        topic_id = button_text_topics_ids[topic_id_name]
        topic_row = topic_button_textes[topic_id][0][lang]

        second_row = ""
        if topic_id_name == "ct_cmp_or_drm_prb" and data.get("campus_or_dormitory"):
            second_row = campus_or_dormitory_text[lang] + data["campus_or_dormitory"]
        elif topic_id_name != "ct_another_prb" and data.get("faculty"):
            faculty_id = button_text_faculties_ids[data["faculty"]]
            second_row = faculty[lang] + faculty_button_textes[faculty_id][0][lang]

        third_row = ""
        if topic_id_name not in ["ct_another_prb", "ct_cmp_or_drm_prb"] and data.get("course"):
            course_id = button_text_courses_ids[data["course"]]
            third_row = course[lang] + course_button_textes[course_id][0][lang]

        return application_sent_text[lang].format(
            user_name=user.full_name if user else "Unknown user",
            user_nick=user.username or "" if user else "",
            user_id=user.id if user else None,
            topic=topic_row,
            second_row=second_row,
            third_row=third_row,
            request_text=data.get("request_text", ""),
        )

    async def review_entry_func(
        self, node: AutoNode, state: FSMContext, user: User | None, text: str | None
    ) -> None:
        await state.update_data(request_text=text)
        data = await state.get_data()

        request_text_to_send = await self.assemble_request(data, user)
        await state.update_data(request_to_send=request_text_to_send)

        lang = await get_lang_from_state(state)

        request_text = await self.assemble_request(data, user, lang)
        await state.update_data(request=request_text)
