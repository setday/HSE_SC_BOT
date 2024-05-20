from aiogram import Router, Bot, F
from aiogram.types import Message
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, Message, ReplyKeyboardRemove, InlineKeyboardMarkup
from aiogram.filters import CommandStart, Command

from Logger.BackChatUtils import send_data_to_back
from .RequestRouterTexts import *
from .RequestRouterKeyboards import get_entry_servey_suggestion_keyboard
from ..MainRouter.MainRouterTexts import button_option_request
from ..RoutersState import BotState

class RequestRouter(Router):
    def __init__(self, bot: Bot) -> None:
        super().__init__()

        self.bot = bot

        self.callback_query.register(self.start_handler, F.data == button_option_request)
        self.callback_query.register(self.cont_handler, F.data == button_option_another)
        self.callback_query.register(self.cont_handler, F.data == button_option_campus)
        self.callback_query.register(self.cont_handler, F.data == button_option_cancel)
        self.callback_query.register(self.cont_handler, F.data == button_option_dormitory)
        self.callback_query.register(self.cont_handler, F.data == button_option_edu)
        self.message.register(self.default_handler, BotState.request)

    async def start_handler(self, callback: CallbackQuery, state: FSMContext) -> None:
        await self.bot.send_message(callback.from_user.id, welcome_text, reply_markup=get_entry_servey_suggestion_keyboard())
        await callback.answer('.')

    async def cont_handler(self, callback: CallbackQuery, state: FSMContext) -> None:
        await state.set_state(BotState.request)

        await self.bot.send_message(callback.from_user.id, welcome_text_2)
        await callback.answer('.')

    async def default_handler(self, message: Message, state: FSMContext) -> None:
        print('New reqest:', message.text)
        
        await state.set_state(BotState.onboardign)

        await message.answer(default_answer)
