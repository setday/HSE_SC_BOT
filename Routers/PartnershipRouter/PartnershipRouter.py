from datetime import datetime, timedelta

from aiogram import Bot
from aiogram.types import User, CallbackQuery
from aiogram.fsm.context import FSMContext

from Utils.BotStorage import BotStorage

from Utils.BackChatUtils import send_request_to_back

from lib.base.AutoNode import AutoNode
from lib.base.AutoRouter import AutoRouter, ExtraAutoNodes

from .PartnershipRouterTexts import *

from Utils.Utils import get_lang_from_state


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
                "user_id": user.id if user else None,
                "topic": "Cooperation",
                "request": data["request"],
            },
            request_id,
        )
        await state.update_data(request_queue=request_queue)
        await state.update_data(request_id=request_id)

        await super().callback_handler(callback, state)
        


class PartnershipRouter(AutoRouter):
    def __init__(self, bot: Bot) -> None:
        super().__init__(bot)
        super().__init__(bot)

        self.create_node(
            "partnership_entry",
            block_enter_text,
            "./Assets/PartnershipProfile.webp",
            parse_mode="HTML",
        ).set_trigger_callback(self.clear_state_func)
        self.create_node(
            "partners_message_review",
            confirm_application_text,
        ).set_trigger_callback(self.review_entry_func)
        self.add_node(
            SenderAutoNode(
                bot,
                self,
                "partners_message_sent",
                reqest_registred_text,
            )
        )

        self.convert_to_entry_node("partnership_entry")

        self.add_message_edge("partnership_entry", "partners_message_review")

        self.add_button_edge(
            "partners_message_review",
            "partners_message_sent",
            button_text_approve_application,
        )
        self.add_button_edge(
            "partners_message_review",
            "partnership_entry",
            button_text_back_to_application,
        )

        self.add_button_edge("partnership_entry", ExtraAutoNodes.HOME_NODE)
        self.add_button_edge("partners_message_sent", ExtraAutoNodes.HOME_NODE)

    async def clear_state_func(
        self, node: AutoNode, state: FSMContext, user: User | None, text: str | None
    ) -> None:
        await state.update_data(
            faculty=None,
            course=None,
            campus_or_dormitory=None,
            request_type=None,
            request=None,
            request_text=None,
            request_to_send=None,
            request_id=None,
        )

    async def review_entry_func(
        self, node: AutoNode, state: FSMContext, user: User | None, text: str | None
    ) -> None:
        lang = await get_lang_from_state(state)

        await state.update_data(request_text=text)
        await state.update_data(
            request_to_send=application_sent_text["ru"].format(
                user_name=user.full_name if user else "Unknown user",
                user_nick=user.username or "" if user else "",
                user_id=user.id if user else None,
                request_text=text,
            )
        )
        await state.update_data(
            request=application_sent_text[lang].format(
                user_name=user.full_name if user else "Unknown user",
                user_nick=user.username or "" if user else "",
                user_id=user.id if user else None,
                request_text=text,
            )
        )
