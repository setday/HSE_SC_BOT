from enum import Enum
from typing import Callable, Coroutine, Any

from aiogram import Router, Bot, F
from aiogram.types import CallbackQuery, Message, User
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from aiogram.types import FSInputFile

from Utils.KeyboardMaker import make_keyboard

from Utils.Utils import answer_callback, get_lang_from_state


class AutoNodeAnswerType(Enum):
    NEW_MESSAGE = 0
    TOAST = 1
    NOTHING = 2


class AutoNode:
    def __init__(
        self,
        bot: Bot,
        router: Router,
        node_name: str,
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
        assert not (
            answer_type == AutoNodeAnswerType.TOAST and media is not None
        ), "Can't send media with toast"

        self._bot: Bot = bot
        self._router: Router = router

        self._node_name: str = node_name
        self._node_state: State | None = None

        self._is_callback_handler_registered: bool = False
        self._is_callback_with_information_handler_registered: bool = False
        self._is_message_handler_registered: bool = False

        self._callback_with_information_destination: str | None = None

        self._text = text
        self._media = media

        self._node_trigger_callback = node_trigger_callback

        self._answer_type = answer_type

        self._message_kwargs = message_kwargs

        self._keyboard_buttons: list[tuple[dict[str, str], str, str | None]] = []

        self._next_node_state: State | None = None

    @property
    def node_name(self) -> str:
        return self._node_name
    
    @property
    def node_state(self) -> State:
        if self._node_state is None:
            self._node_state = State(self._node_name)

        return self._node_state
    
    @property
    def bot(self) -> Bot:
        return self._bot

    @property
    def has_next_message_node(self) -> bool:
        return self._next_node_state is not None
    
    @property
    def has_callback_with_information_handler(self) -> bool:
        return self._is_callback_with_information_handler_registered

    def register_message_handler(self) -> None:
        if not self._is_message_handler_registered:
            self._router.message.register(self.message_handler, self.node_state)
            self._is_message_handler_registered = True

    def register_callback_handler(self) -> None:
        if not self._is_callback_handler_registered:
            self._router.callback_query.register(
                self.callback_handler, F.data == self._node_name
            )
            self._is_callback_handler_registered = True

    def register_callback_with_information_handler(self, destination: str | None = None) -> None:
        if not self._is_callback_with_information_handler_registered:
            self._router.callback_query.register(
                self.callback_handler, F.data.contains(f"{self._node_name}_dr:")
            )
            self._is_callback_with_information_handler_registered = True
            self._callback_with_information_destination = destination

    def add_keyboard_button(
        self, next_node_name: str, button_text: dict[str, str]
    ) -> None:
        assert (
            self._answer_type == AutoNodeAnswerType.NEW_MESSAGE
        ), "Can't add button to toast"

        if next_node_name.startswith("http"):
            self._keyboard_buttons.append(
                (button_text, "url_destination", next_node_name)
            )
        else:
            self._keyboard_buttons.append((button_text, next_node_name, None))

    def add_state_changer(self, next_node_state: State) -> None:
        self._next_node_state = next_node_state

    async def callback_handler(
        self, callback: CallbackQuery, state: FSMContext
    ) -> None:
        if self._node_trigger_callback:
            result = await self._node_trigger_callback(
                self, state, callback.from_user, callback.data
            )

            if result is False:
                return

        if self._next_node_state:
            await state.set_state(self._next_node_state)

        user: User = callback.from_user
        lang: str = await get_lang_from_state(state)
        data = await state.get_data()

        text_to_send: str | None = None
        if self._text:
            text_to_send = self._text[lang]
            text_to_send = text_to_send.format(
                user_name=user.full_name,
                user_nick=user.username or "",
                user_id=user.id,
                **data
            )

        keyboard_buttons: list[tuple[str, str, str | None]] = []
        for button_text, next_node_name, link in self._keyboard_buttons:
            keyboard_buttons.append((button_text[lang], next_node_name, link))

        if self._answer_type == AutoNodeAnswerType.NEW_MESSAGE:
            await callback.answer()

            await answer_callback(
                bot=self._bot,
                callback=callback,
                text=text_to_send,
                reply_markup=make_keyboard(*keyboard_buttons),
                photo=self._media,
                **self._message_kwargs
            )
        elif self._answer_type == AutoNodeAnswerType.TOAST:
            await callback.answer(text=text_to_send or "")
        else:
            raise ValueError("Unknown answer type")
        
    async def callback_with_information_handler(
        self, callback: CallbackQuery, state: FSMContext
    ) -> None:
        if self._callback_with_information_destination:
            data = callback.data.split(":")[-1] if callback.data else None
            await state.update_data({self._callback_with_information_destination: data})

        await self.callback_handler(callback, state)

    async def message_handler(self, message: Message, state: FSMContext) -> None:

        if self._node_trigger_callback:
            result = await self._node_trigger_callback(
                self, state, message.from_user, message.html_text
            )

            if result is False:
                return

        if self._next_node_state:
            await state.set_state(self._next_node_state)

        user: User | None = message.from_user
        lang: str = await get_lang_from_state(state)
        data = await state.get_data()

        text_to_send: str | None = None
        if self._text:
            text_to_send = self._text[lang]
            text_to_send = text_to_send.format(
                user_name=user.full_name if user else "Unknown user",
                user_nick=user.username or "" if user else "",
                user_id=user.id if user else None,
                **data
            )

        keyboard_buttons: list[tuple[str, str, str | None]] = []
        for button_text, next_node_name, link in self._keyboard_buttons:
            keyboard_buttons.append((button_text[lang], next_node_name, link))

        if self._answer_type == AutoNodeAnswerType.NEW_MESSAGE:
            if not self._media:
                await message.answer(
                    text=text_to_send or "No text",
                    reply_markup=make_keyboard(*keyboard_buttons),
                    **self._message_kwargs
                )
            else:
                await self.bot.send_photo(
                    chat_id=message.chat.id,
                    photo=self._media,
                    caption=text_to_send or "",
                    reply_markup=make_keyboard(*keyboard_buttons),
                    **self._message_kwargs
                )
        else:
            raise ValueError("Unknown answer type")
