# Welcome message
block_enter_text = """✨ Привет! На связи официальный Студсовета Питерской Вышки! Пожалуйста, выберите предпочитаемый язык общения:

—

✨ Hi! It's the official Student Council of HSE - St. Petersburg. Please select your preferred language:"""
block_default_text = "Вы хотите создать обращение (нам будет проще решить вопрос если вы сначала выберите категорию)?"
unknown_action_text: dict[str, str] = {
    "ru": "К сожалению, я не знаю что делать с этим сообщением. Попробуйте выбрать один из пунктов",
    "en": "I'm sorry, I don't know what to do with this message. Try selecting one of the items",
}

# Language selection
button_text_lang: dict[str, tuple[str, str]] = {
    "ru": ("Русский ⚪🔵🔴", "ru"),
    "en": ("English 🌍", "en"),
}

# Navigation
navigation_text: dict[str, str] = {
    "ru": "=== Навигация ===",
    "en": "=== Navigation ===",
}

# Navigation buttons
button_text_leave_request_to_sc: dict[str, tuple[str, str]] = {
    "ru": ("Написать обращение в Студсовет 💬", "wrt_to_sc"),
    "en": ("Leave a request for the Student Council 💬", "wrt_to_sc"),
}
button_text_work_with_us: dict[str, tuple[str, str]] = {
    "ru": ("Хочу работать с вами 💼", "wrk_wth_sc"),
    "en": ("I want to work with you 💼", "wrk_wth_sc"),
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

reqest_registred_text = "Обращение зарегистрировано. Спасибо за обращение!"

button_option_request = "Написать обращение"
button_option_info = "Узнать информацию про нас"
button_option_work = "Хочу работать с вами"

button_option_request_alt = "Выбрать категорию обращения"

unknown_user = "Errror: user is unknown"
