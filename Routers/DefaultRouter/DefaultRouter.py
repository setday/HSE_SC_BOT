from re import S
from aiogram import Bot

from lib.base.AutoRouter import AutoRouter
from lib.base.ExtraAutoNodes import DefaultAutoNode, ExtraAutoNodes

from Utils.Filters import SuperChatFilter

from .DefaultRouterTexts import unknown_action_text


class DefaultRouter(AutoRouter):
    def __init__(self, bot: Bot) -> None:
        super().__init__(bot)

        self.add_node(DefaultAutoNode(bot, self, unknown_action_text))

        self.add_button_edge("default_node", ExtraAutoNodes.HOME_NODE)
