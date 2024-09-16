from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from Utils.DefaultTexts import button_text_back_to_main_menu


def make_keyboard(
    *buttons: tuple[str, str, str] | tuple[str, str] | str, sizes: list[int] | None = None
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for button in buttons:
        if isinstance(button, str):
            builder.add(InlineKeyboardButton(text=button, callback_data=button[:30]))
        else:
            url = None if len(button) < 3 else button[2]
            builder.add(InlineKeyboardButton(text=button[0], callback_data=button[1], url=url))

    builder.adjust(*(sizes or [1] * len(buttons)))
    return builder.as_markup()


def make_back_to_main_menu_keyboard(lang: str = "ru") -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.add(
        InlineKeyboardButton(
            text=button_text_back_to_main_menu[lang][0],
            callback_data=button_text_back_to_main_menu[lang][1],
        )
    )

    builder.adjust(1, repeat=True)
    return builder.as_markup()
