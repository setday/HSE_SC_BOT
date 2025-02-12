block_enter_text: dict[str, str] = {
    "ru": """Студенческий совет НИУ ВШЭ — Санкт-Петербург — выборный представительный орган Питерской Вышки и самая внеучебная организация! 

Основная наша задача — помощь студентам вуза на всех уровнях, а также:

• Представление интересов студентов в Учёном Совете НИУ ВШЭ;
• Проведение различных крутых ивентов (<a href="https://vk.com/hsespbstudcouncil">подробнее в ВК!</a>)  
• Участие в решении делегированных Студсовету кейсах (ПГАС, апелляции, дисциплинарные взыскания, социальные вопросы и пр.)

И это только малая часть! Присоединяйся к нам, стань волонтёром или делегатом следующего созыва!""",
    "en": """The Student Council of HSE University in St. Petersburg is the elected representative body of the university and the most non-standard extracurricular organization!

Our main task is to help students of the university at all levels, as well as:

• Representing the interests of students in the Academic Council of HSE University;
• Holding various cool events (<a href="https://vk.com/hsespbstudcouncil">more details in VK!</a>)
• Participation in solving cases delegated to the Student Council (PGAS, appeals, disciplinary actions, social issues, etc.)

And this is only a small part! Join us, become a volunteer or a delegate of the next convocation!""",
}

links_text: dict[str, str] = {
    "ru": '🌐 Сайт: https://spb.hse.ru/studsovet/\n\n📱 <a href="https://vk.com/hsespbstudcouncil">Страничка ВК</a> и <a href="https://t.me/studcouncil">ТГ-канал</a>\n\n✉️ Почта: studsovet.spb@hse.ru',
    "en": '🌐 Webpage: https://spb.hse.ru/studsovet/\n\n📱 <a href="https://vk.com/hsespbstudcouncil">VK page</a> and <a href="https://t.me/studcouncil">TG-channel</a>\n\n✉️ Email: studsovet.spb@hse.ru',
}

faculty_names: dict[str, list[str]] = {
    "ru": [
        "Юриспруденция",
        "Политология и мировая политика",
        "УАГС",
        "Социология и социальная информатика",
        "Межбак по бизнесу и экономике",
        "ПАДиИИ",
        "Медиакоммуникации",
        "Дизайн",
        "Востоковедение",
    ],
    "en": [
        "Law",
        "Political Science and World Politics",
        "Public Policy and Analytics",
        "Sociology and Social Informatics",
        "Interbac",
        "ADAaAI",
        "Media Communications",
        "Design",
        "Asian and African Studies",
    ],
}

committee_names: dict[str, list[str]] = {
    "ru": [
        "Event-менеджмент и PR",
        "HR-комитет",
        "SMM-комитет",
        "Социальный комитет",
        "Правовой комитет",
        "Аналитический комитет",
        "IT-инфраструктура",
        "Дизайнер SMM-комитета",
    ],
    "en": [
        "Event Management and PR Committee",
        "HR Committee",
        "SMM Committee",
        "Social Committee",
        "Legal Committee",
        "Analytical Committee",
        "IT Infrastructure",
        "SMM Committee Designer",
    ],
}

headmaster_member_data_list = [
    [
        "Филиппова София Денисовна",
        "https://vk.com/filizhopss",
        "https://t.me/filizhops",
        "Юриспруденция",
        "Председатель",
        "Filippova Sofia Denisovna",
        "Law",
        "Chairman",
    ],
    [
        "Майков Андрей Владимирович",
        "https://vk.com/steeninfo",
        "https://t.me/steeninfo",
        "Политология и мировая политика",
        "Секретарь",
        "Maykov Andrey Vladimirovich",
        "Political Science and World Politics",
        "Secretary",
    ],
]

head_member_data_list = []

other_member_data_list = [
    [
	    "Смирнова Анастасия",
        "https://vk.com/prostomuka",
        "https://t.me/prostiik",
        "Юриспруденция",
        "Глава правового комитета / Ответственная за СММ",
        "Smirnova Anastasia",
        "Law",
        "Head of the law committee / Responsible for SMM",
    ], [
    	"Якимович Сергей",
        "https://vk.com/se.yakimovich",
        "https://t.me/se_yakimovich",
        "Международный бакалавриат по бизнесу и экономике",
        "Ответственный за качество образования",
        "Yakimovich Sergey",
        "IBBE",
        "Responsible for the quality of education",
    ], [
        "Горшков Максим",
        "https://vk.com/flihten",
        "https://t.me/KiJhoTo",
        "Политология и мировая политика",
        "Ответственный за внешние связи",
        "Maxim Gorshkov",
        "Political Science and World Politics",
        "Responsible for external relations",
    ], [
	    "Сизова Ольга",
        "https://vk.com/osvloz",
        "https://t.me/Olllgessa",
        "Социология и социальная информатика",
        "Ответственный за СММ",
        "Sizova Olga",
        "Sociology and Social Informatics",
        "Responsible for SMM",
    ], [
        "Богосьян Софья",
        "https://vk.com/sofia_bogosyan",
        "https://t.me/Sfbgs",
        "Аналитика в экономике",
        "Делегат в БСС (Большой Студенческий Совет)",
        "Bogosyan Sofia",
        "Economic Data Analytics",
        "Delegate to the BSC (Big Student Council)",
    ], [
        "Архипов Данил",
        "https://vk.com/capnsoth",
        "https://t.me/capnsoth",
        "Юриспруденция",
        "Делегат в БСС / Ответственный за социальные вопросы",
        "Arkhipov Danil",
        "Law",
        "Delegate to the BSC / Responsible for social issues",
    ], [
        "Попов Кирилл",
        "https://vk.com/krilllllmozgyi",
        "https://t.me/kirillpoov",
        "Межбак по бизнесу и экономике",
        "Делегат",
        "Popov Kirill",
        "IBBE",
        "Delegate",
    ], [
        "Султанов Роберт",
        "https://vk.com/cxld.ribs",
        "https://t.me/cxld_ribs",
        "Управление бизнесом",
        "Делегат",
        "Sultanov Robert",
        "Business Administration",
        "Delegate",
    ], [
        "Эноумани Сэмюэл",
        "https://vk.com/mrwisdom96",
        "t.me/PrinceSamuelAyuk",
        "Международный бизнес в Азиатско-Тихоокеанском регионе",
        "Делегат",
        "Enowmanyi Samuel Ayuk",
        "International Business in the Asia-Pacific Region",
        "Delegate",
    ]
]

members_text: dict[str, str] = {
    "ru": "".join(
        [
            "┌── Председатель и секретарь ──\n│\n",
            *[
                f"├ {member[4]} — [{member[0]}]({member[1]}) («{member[3]}»)\n"
                for member in headmaster_member_data_list
            ],
            # "\n┌── Главы комитетов ──\n│\n",
            # *[
            #     f"├ {member[4]} — [{member[0]}]({member[1]}) («{member[3]}»)\n"
            #     for member in head_member_data_list
            # ],
            "\n",
            *[
                f"├ {member[4]} — [{member[0]}]({member[1]}) («{member[3]}»)\n"
                for member in other_member_data_list
            ],
        ]
    ),
    "en": "".join(
        [
            "┌── President and Secretary ──\n│\n",
            *[
                f"├ {member[7]} — [{member[5]}]({member[1]}) («{member[6]}»)\n"
                for member in headmaster_member_data_list
            ],
            # "\n┌── Heads of Committees ──\n│\n",
            # *[
            #     f"├ {member[7]} — [{member[5]}]({member[1]}) («{member[6]}»)\n"
            #     for member in head_member_data_list
            # ],
            "\n",
            *[
                f"├ {member[7]} — [{member[5]}]({member[1]}) («{member[6]}»)\n"
                for member in other_member_data_list
            ],
        ]
    ),
}


button_text_member_list: dict[str, str] = {
    "ru": "Состав 👥",
    "en": "Members 👥",
}
button_text_links: dict[str, str] = {
    "ru": "Ссылки 🔗",
    "en": "Links 🔗",
}
