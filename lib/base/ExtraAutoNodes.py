from enum import Enum
from typing import Callable, Coroutine, Any

from aiogram import Router, Bot
from aiogram.types import User
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile
from aiogram.filters import CommandStart

from lib.base.AutoNode import AutoNode, AutoNodeAnswerType


class ExtraAutoNodes(Enum):
    HOME_NODE = "home_node"


class EntryAutoNode(AutoNode):
    def __init__(
        self,
        bot: Bot,
        router: Router,
        text: dict[str, str] | None = None,
        media: FSInputFile | None = None,
        node_trigger_callback: (
            Callable[
                ["AutoNode", FSMContext, User | None, str | None],
                Coroutine[Any, Any, bool | None],
            ]
            | None
        ) = None,
        answer_type: AutoNodeAnswerType = AutoNodeAnswerType.NEW_MESSAGE,
        **message_kwargs
    ) -> None:
        super().__init__(
            bot,
            router,
            ExtraAutoNodes.HOME_NODE.value,
            text,
            media,
            node_trigger_callback,
            answer_type,
            **message_kwargs
        )

        self._router.message.register(self.message_handler, CommandStart())
        self._is_message_handler_registered = True

        self.register_callback_handler()
