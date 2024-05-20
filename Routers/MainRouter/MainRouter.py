from aiogram import Router, Bot, F
from aiogram.types import Message
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart, Command

from Logger.BackChatUtils import send_data_to_back
from .MainRouterKeyboards import get_entry_servey_suggestion_keyboard
from .MainRouterTexts import welcome_text, default_answer
from ..RoutersState import BotState

class MainRouter(Router):
    def __init__(self, bot: Bot) -> None:
        super().__init__()

        self.bot = bot

        self.message.register(self.start_handler, CommandStart())
        self.message.register(self.default_handler)

    async def start_handler(self, message: Message, state: FSMContext) -> None:
        print('New user:', message.from_user, message.chat.id)

        await state.set_state(BotState.onboardign)

        await message.answer(welcome_text, reply_markup=get_entry_servey_suggestion_keyboard())

    async def default_handler(self, message: Message) -> None:
        await message.answer(default_answer)
