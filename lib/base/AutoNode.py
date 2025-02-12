from enum import Enum
from typing import Callable, Coroutine, Any

from aiogram import Router, Bot, F
from aiogram.types import CallbackQuery, Message, User, InlineKeyboardMarkup, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from aiogram.fsm.storage.base import BaseStorage
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import BaseFilter

from Utils.KeyboardMaker import make_keyboard

from Utils.Utils import answer_callback, get_lang_from_state


void_state = State("void")


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

        self._in_data_endpoints: dict[str | State, str] = {}

        self._text = text
        self._media = media

        self._node_trigger_callback: Callable[
            ["AutoNode", FSMContext, User | None, str | None],
            Coroutine[Any, Any, bool | None],
        ] | None = None
        self._filters: list[BaseFilter] = []

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
    
    @property
    def media(self) -> FSInputFile | None:
        return self._media

    @media.setter
    def media(self, media: FSInputFile | None) -> None:
        self._media = media

    @property
    def text(self) -> dict[str, str] | None:
        return self._text
    
    @text.setter
    def text(self, text: dict[str, str] | None) -> None:
        self._text = text
    
    def set_trigger_callback(
        self,
        node_trigger_callback: Callable[
            ["AutoNode", FSMContext, User | None, str | None],
            Coroutine[Any, Any, bool | None],
        ],
    ) -> "AutoNode":
        self._node_trigger_callback = node_trigger_callback

        return self
    
    def add_filter(self, filter_: BaseFilter) -> "AutoNode":
        self._filters.append(filter_)

        return self
    
    def _prepare_text_to_send(self, lang: str, user: User | None, data: dict) -> str:
        if not self._text or lang not in self._text:
            return ""
        
        translated_text = self._text[lang]
        formated_text = translated_text.format(
            user_name=user.full_name if user else "Unknown user",
            user_nick=user.username or "" if user else "",
            user_id=user.id if user else None,
            **data
        )

        return formated_text
    
    def _prepare_keyboard_buttons(self, lang: str) -> InlineKeyboardMarkup:
        keyboard_buttons = []

        for button_text, next_node_name, link in self._keyboard_buttons:
            keyboard_buttons.append((button_text[lang], next_node_name, link))
        
        keyboard = make_keyboard(*keyboard_buttons)

        return keyboard

    def register_message_handler(self, destination: str | None = None) -> State:
        if not self._is_message_handler_registered:
            self._router.message.register(self.message_handler, self.node_state, *self._filters)
            self._is_message_handler_registered = True

        if destination is None:
            return self.node_state
        
        endpoint = f"{self._node_name}_dr:{len(self._in_data_endpoints)}"
        new_node_endpoint = State(endpoint)
        self._router.message.register(self.message_handler, new_node_endpoint, *self._filters)
        self._in_data_endpoints[new_node_endpoint] = destination

        return new_node_endpoint

    def register_callback_handler(self) -> None:
        if not self._is_callback_handler_registered:
            self._router.callback_query.register(
                self.callback_handler, F.data == self._node_name, *self._filters
            )
            self._is_callback_handler_registered = True

    def register_callback_with_information_handler(self, destination: str | None = None) -> str | None:
        if not self._is_callback_with_information_handler_registered:
            self._router.callback_query.register(
                self.callback_with_information_handler, F.data.startswith(f"{self._node_name}_dr:"), *self._filters
            )
            self._is_callback_with_information_handler_registered = True

        if destination is None:
            return None

        endpoint = f"{self._node_name}_dr:{len(self._in_data_endpoints)}"
        self._in_data_endpoints[endpoint] = destination

        return endpoint

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

        await state.set_state(self._next_node_state or void_state)

        user: User = callback.from_user
        data = await state.get_data()
        lang: str = await get_lang_from_state(state)

        text_to_send = self._prepare_text_to_send(lang, user, data)
        keyboard = self._prepare_keyboard_buttons(lang)

        if self._answer_type == AutoNodeAnswerType.NEW_MESSAGE:
            await callback.answer()

            await answer_callback(
                bot=self._bot,
                callback=callback,
                text=text_to_send,
                reply_markup=keyboard,
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
        if callback.data is None:
            await self.callback_handler(callback, state)
            return

        endpoint_and_data = callback.data.rsplit(":", 1)
        destination = self._in_data_endpoints.get(endpoint_and_data[0], None)

        if len(endpoint_and_data) == 1 or destination is None:
            await self.callback_handler(callback, state)
            return

        await state.update_data({destination: endpoint_and_data[1]})

        await self.callback_handler(callback, state)

    async def message_handler(self, message: Message, state: FSMContext) -> None:
        if message.html_text:
            await state.update_data(attached_photos=[])
            await state.update_data(attached_files=[])

        if message.photo:
            attached_photos = await state.get_value("attached_photos", [])
            if len(attached_photos) < 15:
                attached_photos.append(message.photo[-1].file_id)
                attached_photos = list(set(attached_photos))
                await state.update_data(attached_photos=attached_photos)

        if message.document:
            attached_files = await state.get_value("attached_files", [])
            if len(attached_files) < 15:
                attached_files.append(message.document.file_id)
                attached_files = list(set(attached_files))
                await state.update_data(attached_files=attached_files)

        if not message.html_text:
            return

        graph_state = await state.get_state()
        if graph_state in self._in_data_endpoints:
            await state.update_data({self._in_data_endpoints[graph_state]: message.html_text})

        if self._node_trigger_callback:
            result = await self._node_trigger_callback(
                self, state, message.from_user, message.html_text
            )

            if result is False:
                return

        await state.set_state(self._next_node_state or void_state)

        user: User | None = message.from_user
        data = await state.get_data()
        lang: str = await get_lang_from_state(state)
 
        text_to_send = self._prepare_text_to_send(lang, user, data)
        keyboard = self._prepare_keyboard_buttons(lang)

        if self._answer_type == AutoNodeAnswerType.NEW_MESSAGE:
            if not self._media:
                await message.answer(
                    text=text_to_send or "No text",
                    reply_markup=keyboard,
                    **self._message_kwargs
                )
            else:
                await self.bot.send_photo(
                    chat_id=message.chat.id,
                    photo=self._media,
                    caption=text_to_send or "",
                    reply_markup=keyboard,
                    **self._message_kwargs
                )
        else:
            raise ValueError("Unknown answer type")
        
    async def send_to_user(self, state: FSMContext, user: User) -> None:
        data = await state.get_data()
        lang = await get_lang_from_state(state)

        text_to_send = self._prepare_text_to_send(lang, user, data)
        keyboard_buttons = self._prepare_keyboard_buttons(lang)

        if self._answer_type == AutoNodeAnswerType.NEW_MESSAGE:
            if not self._media:
                await self.bot.send_message(
                    chat_id=user.id,
                    text=text_to_send or "",
                    reply_markup=keyboard_buttons,
                    **self._message_kwargs
                )
            else:
                await self.bot.send_photo(
                    chat_id=user.id,
                    photo=self._media,
                    caption=text_to_send or "",
                    reply_markup=keyboard_buttons,
                    **self._message_kwargs
                )
        else:
            raise ValueError("Unknown answer type")
        
    async def broadcast_message(self, storage: BaseStorage) -> None:
        if not isinstance(storage, MemoryStorage):
            raise ValueError("Currently only MemoryStorage is supported")

        users = storage.storage.keys()
        broadcasted_users = set()

        for user in users:
            if user in broadcasted_users:
                continue
            user_id = user.user_id
            state = FSMContext(storage, user)
            await self.send_to_user(state, User(id=user_id, is_bot=False, first_name=""))
            broadcasted_users.add(user)
