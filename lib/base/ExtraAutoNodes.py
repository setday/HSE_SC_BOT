from enum import Enum
from typing import Callable, Coroutine, Any

from aiogram import Router, Bot
from aiogram.types import User, CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile
from aiogram.filters import BaseFilter, CommandStart

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
        answer_type: AutoNodeAnswerType = AutoNodeAnswerType.NEW_MESSAGE,
        filters: list[BaseFilter] = [],
        **message_kwargs
    ) -> None:
        super().__init__(
            bot,
            router,
            ExtraAutoNodes.HOME_NODE.value,
            text,
            media,
            answer_type,
            **message_kwargs
        )

        self._filters = filters

        self._router.message.register(self.message_handler, CommandStart(), *self._filters)
        self._is_message_handler_registered = True

        self.register_callback_handler()

    def add_filter(self, filter_: BaseFilter) -> AutoNode:
        raise NotImplementedError("Filters should be set in the constructor")


class MappingCallbackAutoNode(AutoNode):
    def __init__(self, bot: Bot, router: Router, node_name: str, mapping: dict[str | None, AutoNode]) -> None:
        super().__init__(bot, router, node_name)
        self._mapping = mapping

    async def callback_handler(self, callback: CallbackQuery, state: FSMContext) -> None:
        await self._mapping[callback.data].callback_handler(callback, state)

    async def message_handler(self, message: Message, state: FSMContext) -> None:
        raise NotImplementedError("MappingCallbackAutoNode does not support message_handler")


class DefaultAutoNode(AutoNode):
    def __init__(self, bot: Bot, router: Router, text: dict[str, str] | None = None, filters: list[BaseFilter] = []) -> None:
        super().__init__(bot, router, "default_node", text)

        self._filters = filters

        self._router.callback_query.register(self.callback_handler, *self._filters)
        self._is_callback_handler_registered = True

        self._router.message.register(self.message_handler, *self._filters)
        self._is_message_handler_registered = True

    def add_filter(self, filter_: BaseFilter) -> AutoNode:
        raise NotImplementedError("Filters should be set in the constructor")

    def register_message_handler(self) -> None:
        raise NotImplementedError("This node is already handling all messages")
    
    def register_callback_handler(self) -> None:
        raise NotImplementedError("This node is already handling all callbacks")
    
    def register_callback_with_information_handler(self) -> None:
        raise NotImplementedError("This node is already handling all callbacks with information")

    async def callback_handler(self, callback: CallbackQuery, state: FSMContext) -> None:
        print("Unhandeled callback:", callback.data)

        await super().callback_handler(callback, state)

    async def message_handler(self, message: Message, state: FSMContext) -> None:
        print(
            "Unhandeled message:",
            message.text,
            " | DOC -> | ",
            message.document,
            " | MIM -> | ",
            message.document.mime_type if message.document else None,
            " | MID -> | ",
            message.media_group_id,
            " | CID -> | ",
            message.chat.id,
        )

        await super().message_handler(message, state)
