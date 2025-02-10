chat_id_text = "ID твоего чата: {0}"
bot_id_text = "ID бота: {0}"
fsm_state_text = "Твой state: {0}\nТвои данные: {1}"

facts_format_text: dict[str, str] = {
    "ru": "Интересный факт №{0}:\n\n",
    "en": "Interesting fact №{0}:\n\n",
}

facts_text: dict[str, list[str]] = {
    "ru":[
        "Ты нашёл секретный факт!\n\nТвой код: {0}",
        "Самым сложным при создании бота было не написание кода и не создание его структуры, а написание описания Студсовета 😁",
        "Для того, чтобы улучшить свои оценки нужно просто принести на экзамен ..... себя с выученным материалом",
        "Изначально эта секция не планировалась, но разрабу показалось, что это привлечёт людей =)",
        "??? Если прописать эту команду 19 числа ровно в 04:04, то можно получить секретный код, но зачем он нужен... ???",
        "Изначально над ботом работал только один человек. Сейчас над ним работает пол команды Студсовета, начиная от комитета Event-менеджмента и PR, заканчивая SMM-отделом",
        "Изначально в Студсовет было избрано 24 делегатов, но со временем их количество сократилось до 17, зато появилось очень много волонтеров 😊",
        "В боте есть баг, но разработчик его не нашел 😈",
        "В боте есть дополнительный функционал, но он доступен не всем.",
        "Файл с этими фактами доступен на GitHub и его можно попробовать найти, чтобы не перебирать все факты =]",
        "Мы планируем написать ещё одного бота, но зачем он будет нужен, вы узнаете позже =)",
        "В апреле мы планируем запустить криптовалюту, но вам об этом не расскажем =D",
        "Мы так и не определились с картинками =D",
    ],
    "en":[
        "You found a secret fact!\n\nYour code: {0}",
        "The most difficult thing in creating a bot was not writing the code and not creating its structure, but writing a description of the Student Council 😁",
        "In order to improve your grades, you just need to bring to the exam ..... yourself with the material learned",
        "Initially, this section was not planned, but the developer thought that it would attract people =)",
        "??? If you enter this command on the 19th at exactly 04:04, you can get a secret code, but why do you need it... ???",
        "Initially, only one person worked on the bot. Now half of the Student Council team is working on it, starting with the Event Management and PR committee and ending with the SMM department",
        "Initially, 24 delegates were elected to the Student Council, but over time their number decreased to 17, but a lot of volunteers appeared 😊",
        "The bot has a bug, but the developer did not find it 😈",
        "The bot has additional functionality, but it is not available to everyone.",
        "The file with these facts is available on GitHub and you can try to find it so as not to go through all the facts =]",
        "We plan to write another bot, but why it will be needed, you will find out later =)",
        "In April, we plan to launch a cryptocurrency, but we won't tell you about it =D",
        "We still haven't decided on the pictures =D",
    ],
}

credits_text: dict[str, str] = {
    "ru": """Участвовали в запуске бота:

• Архипов Данил - идея создания проекта | разработка архитектуры | решение административных вопросов
• Александр Серков - написание кода | разработка архитектуры
• Горшков Максим - поиск и организация хостинга | установление партнёрских связей с Selectel | тестирование и запуск бота | информационное сопровождение
• Матвеев Анатолий - шикарный дизайн

Отдельное спасибо Selectel за предоставленный хостинг и всем, кто поддерживал проект, занимался его тестированием и предлагал идеи!""",
    "en": """Participated in the launch of the bot:

• Arhipov Danil - idea of creating the project | architecture development | solution of administrative issues
• Alexander Serkov - code writing | architecture development
• Gorshkov Maxim - search and organization of hosting | establishment of partnership relations with Selectel | testing and launching the bot | informational support
• Matveev Anatoly - cool design

Special thanks to Selectel for providing hosting and to everyone who supported the project, tested it and suggested ideas!""",
}