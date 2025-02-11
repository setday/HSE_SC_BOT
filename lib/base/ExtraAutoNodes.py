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


class DefaultAutoNode(AutoNode):
    def __init__(self, bot: Bot, router: Router, text: dict[str, str] | None = None) -> None:
        super().__init__(bot, router, "default_node", text)

        self._router.callback_query.register(self.callback_handler)
        self._is_callback_handler_registered = True

        self._router.message.register(self.message_handler)
        self._is_message_handler_registered = True

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
