from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from Routers.DefaultTexts import back_text

def make_keyboard(*buttons: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    for button in buttons:
        builder.add(InlineKeyboardButton(
            text=button,
            callback_data=button[:30]
        ))

    builder.adjust(1, repeat=True)
    return builder.as_markup()

def make_back_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    builder.add(InlineKeyboardButton(
        text=back_text,
        callback_data=back_text
    ))

    builder.adjust(1, repeat=True)
    return builder.as_markup()
