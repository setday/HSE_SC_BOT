from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from .RequestRouterTexts import *

def get_entry_servey_suggestion_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    # builder.add(InlineKeyboardButton(
    #     text=button_option_edu,
    #     callback_data=button_option_edu
    # ))
    # builder.add(InlineKeyboardButton(
    #     text=button_option_cancel,
    #     callback_data=button_option_cancel
    # ))
    builder.add(InlineKeyboardButton(
        text=button_option_campus,
        callback_data=button_option_campus
    ))
    builder.add(InlineKeyboardButton(
        text=button_option_dormitory,
        callback_data=button_option_dormitory
    ))
    builder.add(InlineKeyboardButton(
        text=button_option_another,
        callback_data=button_option_another
    ))
    builder.adjust(1, 1, 1)
    return builder.as_markup()
