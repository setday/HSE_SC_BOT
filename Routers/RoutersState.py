from aiogram.fsm.state import StatesGroup, State


class BotState(StatesGroup):
    onboardign = State()
    work = State()
    info = State()
    request = State()
