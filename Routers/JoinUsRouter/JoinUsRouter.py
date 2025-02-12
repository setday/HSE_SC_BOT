from aiogram import Bot

from config import config

from lib.base.AutoNode import AutoNodeAnswerType
from lib.base.AutoRouter import AutoRouter, ExtraAutoNodes

from .JoinUsRouterTexts import *


class JoinUsRouter(AutoRouter):
    def __init__(self, bot: Bot) -> None:
        super().__init__(bot)

        # delegate_link = "https://forms.gle/Chfps8LqVsWYiCby8" # Invalide for now (volunteer link)
        # volunteer_link = "https://forms.gle/Chfps8LqVsWYiCby8" # Invalide for now (expired at 20.09.2024)

        # ..._uu - Both delegate and volunteer are unavailable
        # ..._vu - Volunteer is available, delegate is unavailable
        # ..._uv - Delegate is available, volunteer is unavailable
        # ..._av - Both delegate and volunteer are available
        self.entry = self.create_node("join_us_entry", block_enter_text_uu, config.posters_dir / "WorkWithUsProfile.webp")
        self.create_node(
            "join_us_unavailable",
            option_is_temporarily_unavailable_text,
            answer_type=AutoNodeAnswerType.TOAST,
        )

        self.convert_to_entry_node("join_us_entry")

        self.add_button_edge("join_us_entry", "join_us_unavailable", button_text_become_delegate_u)
        # self.add_button_edge(ju_entry_name, volunteer_link, button_text_become_delegate_a)

        self.add_button_edge("join_us_entry", "join_us_unavailable", button_text_become_volunteer_u)
        # self.add_button_edge(ju_entry_name, delegate_link, button_text_become_volunteer_a)

        self.add_button_edge("join_us_entry", ExtraAutoNodes.HOME_NODE)

    def reload_assets(self) -> None:
        self.entry.media = self._load_media(config.posters_dir / "WorkWithUsProfile.webp")

        return super().reload_assets()
