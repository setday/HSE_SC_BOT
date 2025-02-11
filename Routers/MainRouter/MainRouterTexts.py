# Welcome message
block_enter_text: str = """✨ Привет! На связи официальный чат-бот Студсовета Питерской Вышки! Пожалуйста, выбери предпочитаемый язык общения:

—

✨ Hi! It's the official chatbot of the Student Council of HSE SPb! Please select your preferred language:"""

# Language selection
language_selection_text: dict[str, str] = {
    "en": "Select the language:",
    "ru": "Выбери язык общения:",
}

change_language_button_textes: list[dict[str, str]] = [
    {
        "en": "Русский ⚪🔵🔴",
        "ru": "Русский ⚪🔵🔴",
    },
    {
        "en": "English 🌍",
        "ru": "English 🌍",
    },
]
language_list: list[str] = ["ru", "en"]

# Navigation
navigation_text: dict[str, str] = {
    "ru": "Навигация",
    "en": "Navigation",
}

# Navigation buttons
button_text_leave_request_to_sc: dict[str, str] = {
    "ru": "Написать обращение в Студсовет 💬",
    "en": "Leave a request for the Student Council 💬",
}
button_text_work_with_us: dict[str, str] = {
    "ru": "Присоединиться к нам 💼",
    "en": "Join us 💼",
}
button_text_info_about_sc: dict[str, str] = {
    "ru": "Информация про нас 🤓",
    "en": "Information about us 🤓",
}
button_text_change_language: dict[str, str] = {
    "ru": "Change the language 🌍",
    "en": "Изменить язык общения бота 🌍",
}
button_text_partnership: dict[str, str] = {
    "ru": "Сотрудничество 🤝",
    "en": "Partnership 🤝",
}

unknown_user = "Errror: user is unknown"
