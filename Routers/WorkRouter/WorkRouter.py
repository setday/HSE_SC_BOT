from aiogram import Router, Bot, F
from aiogram.types import Message
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, Message, ReplyKeyboardRemove, InlineKeyboardMarkup
from aiogram.filters import CommandStart, Command

from Logger.BackChatUtils import send_data_to_back
from .WorkRouterTexts import welcome_text, default_answer
from ..MainRouter.MainRouterTexts import button_option_work
from ..RoutersState import BotState

class WorkRouter(Router):
    def __init__(self, bot: Bot) -> None:
        super().__init__()

        self.bot = bot

        self.callback_query.register(self.start_handler, F.data == button_option_work)
        self.message.register(self.default_handler, BotState.work)

    async def start_handler(self, callback: CallbackQuery, state: FSMContext) -> None:
        await state.set_state(BotState.work)

        await self.bot.send_message(callback.from_user.id, welcome_text)
        await callback.answer('Поехали!')

    async def default_handler(self, message: Message, state: FSMContext) -> None:
        print('New work:', message.text)
        
        await state.set_state(BotState.onboardign)

        await message.answer(default_answer)
