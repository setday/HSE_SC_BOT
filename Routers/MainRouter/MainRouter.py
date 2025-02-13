from aiogram import Bot
from aiogram.types import User
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile

from config import config

from lib.base.AutoNode import AutoNode
from lib.base.ExtraAutoNodes import EntryAutoNode, ExtraAutoNodes
from lib.base.AutoRouter import AutoRouter

from Utils.Filters import SuperChatFilter

from .MainRouterTexts import *
from Routers.Events.valentinesDay.ValentinesDayRouterTexts import valentine_send_button_text

from Utils.Utils import check_lang_in_state


class MainRouter(AutoRouter):
    def __init__(self, bot: Bot) -> None:
        super().__init__(bot)

        self.entry = EntryAutoNode(
                bot, self,
                text=navigation_text,
                media=FSInputFile(config.posters_dir / "GlobalProfile.webp"),
                filters=[SuperChatFilter(False)]
        ).set_trigger_callback(self.entry_action)

        self.add_node(self.entry)
        self.create_node("language_selection", language_selection_text)

        ### Event edges

        self.valentines_day_edge = self.add_button_edge(ExtraAutoNodes.HOME_NODE.value, "valentines_day_entry", valentine_send_button_text, is_next_node_local=False) or ""
        self.toggle_edge(self.valentines_day_edge, False)

        ### Normal edges

        self.add_button_edge(ExtraAutoNodes.HOME_NODE.value, "info_entry", button_text_info_about_sc, is_next_node_local=False)
        self.add_button_edge(ExtraAutoNodes.HOME_NODE.value, "leave_request_entry", button_text_leave_request_to_sc, is_next_node_local=False)
        self.add_button_edge(ExtraAutoNodes.HOME_NODE.value, "join_us_entry", button_text_work_with_us, is_next_node_local=False)
        self.add_button_edge(ExtraAutoNodes.HOME_NODE.value, "partnership_entry", button_text_partnership, is_next_node_local=False)

        self.add_button_edge(ExtraAutoNodes.HOME_NODE.value, "language_selection", button_text_change_language)
        self.add_selector_edge("language_selection", ExtraAutoNodes.HOME_NODE.value, change_language_button_textes, state_destination="language")

        self.convert_to_entry_node(ExtraAutoNodes.HOME_NODE.value)

    def reload_assets(self) -> None:
        self.entry.media = self._load_media(config.posters_dir / "GlobalProfile.webp")

        if config.current_event == "valentines_day":
            self.toggle_edge(self.valentines_day_edge, True)
        else:
            self.toggle_edge(self.valentines_day_edge, False)


        return super().reload_assets()

    async def entry_action(
        self, node: AutoNode, state: FSMContext, user: User | None, text: str | None
    ) -> None:
        if text == "/start" and not await check_lang_in_state(state):
            lang = "ru"
            if user and user.language_code:
                lang = user.language_code
            if lang not in language_list:
                lang = "en"
            await state.update_data(language=lang)
