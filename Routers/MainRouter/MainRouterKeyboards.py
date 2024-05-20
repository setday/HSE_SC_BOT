from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from .MainRouterTexts import button_option_info, button_option_request, button_option_work

def get_entry_servey_suggestion_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text=button_option_request,
        callback_data=button_option_request
    ))
    builder.add(InlineKeyboardButton(
        text=button_option_info,
        callback_data=button_option_info
    ))
    builder.add(InlineKeyboardButton(
        text=button_option_work,
        callback_data=button_option_work
    ))
    builder.adjust(1, 1, 1)
    return builder.as_markup()
