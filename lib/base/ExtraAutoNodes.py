from enum import Enum
from typing import Callable, Coroutine, Any

from aiogram import Router, Bot
from aiogram.types import User, CallbackQuery, Message
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
        
class MappingCallbackAutoNode(AutoNode):
    def __init__(self, bot: Bot, router: Router, node_name: str, mapping: dict[str | None, AutoNode]) -> None:
        super().__init__(bot, router, node_name)
        self._mapping = mapping

    async def callback_handler(self, callback: CallbackQuery, state: FSMContext) -> None:
        await self._mapping[callback.data].callback_handler(callback, state)

    async def message_handler(self, message: Message, state: FSMContext) -> None:
        raise NotImplementedError("MappingCallbackAutoNode does not support message_handler")
