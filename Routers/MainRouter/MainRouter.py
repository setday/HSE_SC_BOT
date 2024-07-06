from ast import main
from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import StatesGroup, State

from Routers.DefaultTexts import send_text, sent_text, cancel_text, back_text, back_to_menu_text, get_lang_from_state, button_text_back_to_main_menu
from Routers.KeyboardMaker import make_keyboard, make_back_keyboard

from Logger.BackChatUtils import send_data_to_back
from .MainRouterTexts import *

from ..Utils import answer_callback

class MainRouterState(StatesGroup):
    language_selection = State()
    main_menu = State()
    default = State()

class MainRouter(Router):
    def __init__(self, bot: Bot) -> None:
        super().__init__()

        self.bot = bot

        self.message.register(self.get_chat_id_hnadler, Command("get_chat_id"))

        self.message.register(self.enter_handler, CommandStart())
        self.callback_query.register(self.language_selection_handler, F.data == button_text_change_language["en"][1])
        self.callback_query.register(self.language_selected_handler, MainRouterState.language_selection)
        self.callback_query.register(self.main_menu_handler, F.data == button_text_back_to_main_menu["en"][1])
        
        self.callback_query.register(self.enter_callback_handler, F.data == back_text)
        self.callback_query.register(self.enter_callback_handler, F.data == cancel_text)
        self.callback_query.register(self.enter_callback_handler, F.data == back_to_menu_text)
        self.callback_query.register(self.send_handler, F.data == send_text)

        self.message.register(self.default_reqest_handler, MainRouterState.default)
        self.message.register(self.default_handler)
        self.callback_query.register(self.default_callback_handler)

    async def get_chat_id_hnadler(self, message: Message) -> None:
        await message.answer(str(message.chat.id))

    async def default_handler(self, message: Message, state: FSMContext) -> None:
        print("Unhandeled message:", message.text)
        lang = await get_lang_from_state(state)
        await message.answer(unknown_action_text[lang], reply_markup=make_back_keyboard())

    async def default_callback_handler(self, callback: CallbackQuery, state: FSMContext) -> None:
        print("Unhandeled callback:", callback.data)
        lang = await get_lang_from_state(state)
        await callback.answer(unknown_action_text[lang])
    
    # Enter handlers
    async def enter_handler(self, message: Message, state: FSMContext) -> None:
        status = await state.get_state()
        if status:
            await message.delete()
            return

        await state.set_state(MainRouterState.language_selection)

        await message.answer(block_enter_text, reply_markup=make_keyboard(
            button_text_lang["ru"],
            button_text_lang["en"],
        ))
        
    async def language_selection_handler(self, callback: CallbackQuery, state: FSMContext) -> None:
        await state.set_state(MainRouterState.language_selection)

        await callback.answer()

        await answer_callback(
            bot=self.bot,
            callback=callback,
            text=block_enter_text,
            reply_markup=make_keyboard(
                button_text_lang["ru"],
                button_text_lang["en"],
            )
        )

    async def language_selected_handler(self, callback: CallbackQuery, state: FSMContext) -> None:
        await state.set_state(MainRouterState.main_menu)

        lang = callback.data if callback.data in ["ru", "en"] else "ru"
        await state.update_data(language=lang)

        await self.main_menu_handler(callback, state)

    async def main_menu_handler(self, callback: CallbackQuery, state: FSMContext) -> None:
        await callback.answer()

        lang = await get_lang_from_state(state)

        await answer_callback(
            bot=self.bot,
            callback=callback,
            text=navigation_text[lang],
            reply_markup=make_keyboard(
                button_text_leave_request_to_sc[lang],
                button_text_work_with_us[lang],
                button_text_info_about_sc[lang],
                button_text_change_language[lang],
                button_text_partnership[lang],
        ))

    async def enter_callback_handler(self, callback: CallbackQuery, state: FSMContext) -> None:
        await state.set_state(MainRouterState.default)

        await callback.answer()

        await answer_callback(
            bot=self.bot,
            callback=callback,
            text=block_enter_text,
            reply_markup=make_keyboard(
                button_option_request,
                button_option_info,
                button_option_work
        ))

    async def default_reqest_handler(self, message: Message, state: FSMContext) -> None:
        if not message.from_user:
            await message.answer(unknown_user)
            return

        request_text = f"Обращение от {message.from_user.first_name or ''} {message.from_user.last_name or ''} (@{message.from_user.username or ''}):\n\n{message.html_text}"
        await state.set_data({"request": request_text})

        await message.answer(
            block_default_text + "\n\n-------\n" + request_text + "\n-------",
            reply_markup=make_keyboard(
                button_option_request_alt,
                send_text,
                cancel_text
            ),
            parse_mode="HTML"
        )

    async def send_handler(self, callback: CallbackQuery, state: FSMContext) -> None:
        data = await state.get_data()

        number = await send_data_to_back(self.bot, data["request"])

        await callback.answer(sent_text)

        await answer_callback(
            bot=self.bot,
            callback=callback,
            text=f"Номер обращения - {number}\n\n{reqest_registred_text}",
            reply_markup=make_back_keyboard()
        )
        await state.set_data({})
