from aiogram import Bot

from lib.base.AutoRouter import AutoRouter, ExtraAutoNodes

from .InfoRouterTexts import *
from ..MainRouter.MainRouterTexts import button_text_info_about_sc


class InfoRouter(AutoRouter):
    def __init__(self, bot: Bot) -> None:
        super().__init__(bot)

        info_entry_name = button_text_info_about_sc["en"][1]

        self.add_node(info_entry_name, block_enter_text, "./Assets/AboutUsProfile.webp")
        self.add_node(
            "info_member_list",
            members_text,
            saveMedia=False,
            disable_web_page_preview=True,
            parse_mode="Markdown",
        )
        self.add_node("info_links", links_text)

        self.convert_to_entry_node(info_entry_name)

        self.add_button_edge(
            info_entry_name, "info_member_list", button_text_member_list
        )
        self.add_button_edge(info_entry_name, "info_links", button_text_links)

        self.add_button_edge("info_links", "info_member_list", button_text_member_list)
        self.add_button_edge("info_member_list", "info_links", button_text_links)

        self.add_button_edge(info_entry_name, ExtraAutoNodes.HOME_NODE)
        self.add_button_edge("info_member_list", ExtraAutoNodes.HOME_NODE)
        self.add_button_edge("info_links", ExtraAutoNodes.HOME_NODE)
