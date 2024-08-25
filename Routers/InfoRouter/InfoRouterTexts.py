block_enter_text : dict[str, str] = {
    "ru": "Студенческий совет НИУ ВШЭ – Санкт-Петербург — выборный представительный орган НИУ ВШЭ – Санкт-Петербург. Основная наша задача — представление и отстаивание интересов студентов НИУ ВШЭ – Санкт-Петербург на всех уровнях.\n\nВ компетенцию Студсовета входит рассмотрение, формирование мнения и рекомендаций по всем вопросам, затрагивающим права и законные интересы студентов (повышенные стипендии, общежития, образовательный процесс и т.д.)",
    "en": "The Student Council of HSE University - St. Petersburg is an elected representative body of HSE University - St. Petersburg. Our main task is to represent and defend the interests of students of HSE University - St. Petersburg at all levels.\n\nThe competence of the Student Council includes consideration, formation of opinions and recommendations on all issues affecting the rights and legitimate interests of students (increased scholarships, dormitories, educational process, etc.)",
}

links_text : dict[str, str] = {
    "ru": "Наш сайт: https://spb.hse.ru/studsovet/\n\nНаш ВК: https://vk.com/hsespbstudcouncil\nИ наш тг-канал: https://t.me/studcouncil",
    "en": "Our website: https://spb.hse.ru/studsovet/\n\nOur VK: https://vk.com/hsespbstudcouncil\nAnd our tg-channel: https://t.me/studcouncil",
}

member_data_list = [
    ["Богосьян Лариса Мироновна", "https://vk.com/lrsbog", "https://t.me/lrbog", "4 курс, «Социология и социальная информатика»", "Председатель"],
    ["Саранская Екатерина", "https://vk.com/ekatia17", "https://t.me/ekatia17", "3 курс, «Юриспруденция»", "Секретарь"],
    ["Серков Александр Максимович", "https://vk.com/setday", "https://t.me/", "2 курс, «Прикладной анализ данных и искусственный интеллект»", "IT-инфраструктура"],
    ["Астафьева Елизавета Денисовна", "https://vk.com/asterlissa", "https://t.me/lizastaf", "3 курс, «Филология»", "Глава Медиа-комитета"],
    ["Архипов Данил Владимирович", "https://vk.com/capnsoth", "https://t.me/CapnSoth", "-1 курс, «None»", "Глава HR-комитет"],
    ["Козин Георгий Евгеньевич", "https://vk.com/waitforit", "https://t.me/Wait_For_lt", "-1 курс, «Международный бакалавриат по экономике и бизнесу»", "Глава Научного отдела"],
    ["Сударева Екатерина Михайловна", "https://vk.com/kattyayaa", "https://t.me/kattyyaaa", "-1 курс, «Медиакоммуникации»", "Дизайнер SMM-комитета"],
]

members_text = "".join([
    "Текущий состав:\n\n",
    "".join(['{member[4]} - <a href="{member[1]}">{member[0]}</a> ({member[3]})\n' for member in member_data_list[:1]]),
    "\n",
    "".join(['{member[4]} - <a href="{member[1]}">{member[0]}</a> ({member[3]})\n' for member in member_data_list[1:]]),
])


button_text_member_list : dict[str, tuple[str, str]] = {
    "ru": ("👥 Состав", "mbr_lst"),
    "en": ("👥 Members", "mbr_lst"),
}
button_text_links : dict[str, tuple[str, str]] = {
    "ru": ("🔗 Ссылки", "sc_lnks"),
    "en": ("🔗 Links", "sc_lnks"),
}
