from aiogram import Router, Bot, F
from aiogram.types import Message
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, Message, ReplyKeyboardRemove, InlineKeyboardMarkup
from aiogram.filters import CommandStart, Command

from Logger.BackChatUtils import send_data_to_back
from .InfoRouterTexts import welcome_text
from ..MainRouter.MainRouterTexts import button_option_info
from ..RoutersState import BotState

class InfoRouter(Router):
    def __init__(self, bot: Bot) -> None:
        super().__init__()

        self.bot = bot

        self.callback_query.register(self.start_handler, F.data == button_option_info)

    async def start_handler(self, callback: CallbackQuery, state: FSMContext) -> None:
        await self.bot.send_message(callback.from_user.id, welcome_text)
        await callback.answer('Поехали!')
