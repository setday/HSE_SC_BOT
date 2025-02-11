from aiogram import Bot

from lib.base.AutoRouter import AutoRouter, ExtraAutoNodes

from .InfoRouterTexts import *


class InfoRouter(AutoRouter):
    def __init__(self, bot: Bot) -> None:
        super().__init__(bot)

        self.create_node("info_entry", block_enter_text, "./Assets/AboutUsProfile.webp")
        self.create_node(
            "info_member_list",
            members_text,
            saveMedia=False,
            disable_web_page_preview=True,
            parse_mode="Markdown",
        )
        self.create_node("info_links", links_text)

        self.convert_to_entry_node("info_entry")

        self.add_button_edge("info_entry", "info_member_list", button_text_member_list)
        self.add_button_edge("info_entry", "info_links", button_text_links)

        self.add_button_edge("info_links", "info_member_list", button_text_member_list)
        self.add_button_edge("info_member_list", "info_links", button_text_links)

        self.add_button_edge("info_entry", ExtraAutoNodes.HOME_NODE)
        self.add_button_edge("info_member_list", ExtraAutoNodes.HOME_NODE)
        self.add_button_edge("info_links", ExtraAutoNodes.HOME_NODE)
