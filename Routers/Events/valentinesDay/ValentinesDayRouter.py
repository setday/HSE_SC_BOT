from datetime import datetime, timedelta

from aiogram import Bot
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from config import config

from lib.base.AutoNode import AutoNode
from lib.base.AutoRouter import AutoRouter, ExtraAutoNodes

from Utils.Utils import get_lang_from_state
from Utils.BotStorage import BotStorage
from Utils.BackChatUtils import send_request_to_back

from .ValentinesDayRouterTexts import *


class SenderAutoNode(AutoNode):
    async def callback_handler(
        self, callback: CallbackQuery, state: FSMContext
    ) -> None:
        data = await state.get_data()
        last_valentine = data.get("last_valentine", None)

        if last_valentine and last_valentine > datetime.now() + timedelta(seconds=-6):
            lang = await get_lang_from_state(state)

            await callback.answer(wait_a_little_text[lang])
            return
        
        await send_request_to_back(self.bot, data["valentine_text"])

        await state.update_data(last_valentine = datetime.now())
        await state.update_data(valentine_text = None)

        await super().callback_handler(callback, state)
        

class ValentinesDayRouter(AutoRouter):
    def __init__(self, bot: Bot) -> None:
        super().__init__(bot)

        self.post = self.create_node("valentines_day_post", post_text, config.valentines_day_posters_dir / "ValentineCard.webp")

        self.entry = self.create_node("valentines_day_entry", block_enter_text, config.valentines_day_posters_dir / "ValentineCard.webp")
        self.create_node(
            "valentines_day_review",
            valentine_send_text,
        )
        self.add_node(
            SenderAutoNode(
                bot,
                self,
                "valentines_day_sent",
                valentine_registred_text,
            )
        )
        
        self.convert_to_entry_node("valentines_day_entry")

        self.add_button_edge("valentines_day_post", "valentines_day_entry", valentine_send_button_text)

        self.add_message_edge("valentines_day_entry", "valentines_day_review", state_destination="valentine_text")

        self.add_button_edge(
            "valentines_day_review",
            "valentines_day_sent",
            valentine_send_button_text,
        )
        self.add_button_edge(
            "valentines_day_review",
            "valentines_day_entry",
            change_valentine_text_button_text,
        )
        self.add_button_edge(
            "valentines_day_sent",
            "valentines_day_entry",
            new_valentine_text,
        )

        self.add_button_edge("valentines_day_post", ExtraAutoNodes.HOME_NODE)
        self.add_button_edge("valentines_day_entry", ExtraAutoNodes.HOME_NODE)
        self.add_button_edge("valentines_day_review", ExtraAutoNodes.HOME_NODE)
        self.add_button_edge("valentines_day_sent", ExtraAutoNodes.HOME_NODE)
