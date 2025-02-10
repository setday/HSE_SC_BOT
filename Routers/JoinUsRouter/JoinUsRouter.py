from aiogram import Bot

from .JoinUsRouterTexts import *
from ..MainRouter.MainRouterTexts import button_text_work_with_us

from lib.base.AutoNode import AutoNodeAnswerType
from lib.base.AutoRouter import AutoRouter, ExtraAutoNodes


class JoinUsRouter(AutoRouter):
    def __init__(self, bot: Bot) -> None:
        super().__init__(bot)

        join_us_entry_name = button_text_work_with_us["en"][1]

        # delegate_link = "https://forms.gle/Chfps8LqVsWYiCby8" # Invalide for now (volunteer link)
        # volunteer_link = "https://forms.gle/Chfps8LqVsWYiCby8" # Invalide for now (expired at 20.09.2024)

        # ..._uu - Both delegate and volunteer are unavailable
        # ..._vu - Volunteer is available, delegate is unavailable
        # ..._uv - Delegate is available, volunteer is unavailable
        # ..._av - Both delegate and volunteer are available
        self.add_node(join_us_entry_name, block_enter_text_uu, "./Assets/WorkWithUsProfile.webp")
        self.add_node("join_us_unavailable", option_is_temporarily_unavailable_text, answer_type=AutoNodeAnswerType.TOAST)

        self.convert_to_entry_node(join_us_entry_name)

        self.add_button_edge(join_us_entry_name, "join_us_unavailable", button_text_become_delegate_u)
        # self.add_button_edge(ju_entry_name, volunteer_link, button_text_become_delegate_a)

        self.add_button_edge(join_us_entry_name, "join_us_unavailable", button_text_become_volunteer_u)
        # self.add_button_edge(ju_entry_name, delegate_link, button_text_become_volunteer_a)

        self.add_button_edge(join_us_entry_name, ExtraAutoNodes.HOME_NODE)
