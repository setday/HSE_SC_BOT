# Welcome message
block_enter_text: str = """✨ Привет! На связи официальный чат-бот Студсовета Питерской Вышки! Пожалуйста, выбери предпочитаемый язык общения:

—

✨ Hi! It's the official chatbot of the Student Council of HSE SPb! Please select your preferred language:"""

# Language selection
button_text_lang: dict[str, tuple[str, str]] = {
    "ru": ("Русский ⚪🔵🔴", "chng_lang_ru"),
    "en": ("English 🌍", "chng_lang_en"),
}

button_lang_datas = [lang_data[1] for lang_data in button_text_lang.values()]

# Navigation
navigation_text: dict[str, str] = {
    "ru": "Навигация",
    "en": "Navigation",
}

# Navigation buttons
button_text_leave_request_to_sc: dict[str, tuple[str, str]] = {
    "ru": ("Написать обращение в Студсовет 💬", "wrt_to_sc"),
    "en": ("Leave a request for the Student Council 💬", "wrt_to_sc"),
}
button_text_work_with_us: dict[str, tuple[str, str]] = {
    "ru": ("Присоединиться к нам 💼", "wrk_wth_sc"),
    "en": ("Join us 💼", "wrk_wth_sc"),
}
button_text_info_about_sc: dict[str, tuple[str, str]] = {
    "ru": ("Информация про нас 🤓", "abt_us"),
    "en": ("Information about us 🤓", "abt_us"),
}
button_text_change_language: dict[str, tuple[str, str]] = {
    "ru": ("Change the language 🌍", "lang_chg"),
    "en": ("Изменить язык общения бота 🌍", "lang_chg"),
}
button_text_partnership: dict[str, tuple[str, str]] = {
    "ru": ("Сотрудничество 🤝", "prt_shp"),
    "en": ("Partnership 🤝", "prt_shp"),
}

unknown_user = "Errror: user is unknown"
