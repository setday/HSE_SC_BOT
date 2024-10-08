from Utils.DefaultTexts import button_text_back_to_main_menu

something_went_wrong_text: dict[str, str] = {
    "ru": "❔Что-то пошло не так. Попробуй вернуться в главное меню и попробовать снова.",
    "en": "❔Something went wrong. Try to go back to the main menu and try again.",
}

block_enter_text: dict[str, str] = {
    "ru": "❔По какому поводу обращение?",
    "en": "❔What is your request about?",
}

button_your_requests_text: dict[str, tuple[str, str]] = {
    "ru": ("Твои обращения 👀", "shw_appls"),
    "en": ("Your requests 👀", "shw_appls"),
}
button_text_topics: dict[str, list[tuple[str, str]]] = {
    "ru": [
        ("Присутствие Студсовета на апелляционной комиссии ☎️", "ct_app_com"),
        ("Общежития или корпуса ВШЭ 🏡", "ct_cmp_or_drm_prb"),
        ("Образовательный процесс 📖", "ct_edu_prb"),
        ("Другое 💊", "ct_another_prb"),
        button_your_requests_text["ru"],
        button_text_back_to_main_menu["ru"],
    ],
    "en": [
        (
            "Student Council presence at the appeals commission ☎️",
            "ct_app_com",
        ),
        (
            "Dormitory or HSE campus 🏡",
            "ct_cmp_or_drm_prb",
        ),
        (
            "Educational process 📖",
            "ct_edu_prb",
        ),
        ("Other 💊", "ct_another_prb"),
        button_your_requests_text["en"],
        button_text_back_to_main_menu["en"],
    ],
}
button_text_topics_ids: dict[str, int] = {
    key: i for i, (_, key) in enumerate(button_text_topics["ru"])
}

no_sent_requests_text: dict[str, str] = {
    "ru": "📜 У тебя пока нет обращений!",
    "en": "📜 You have no requests yet!",
}
sent_requests_text: dict[str, str] = {
    "ru": "📜 Твои обращения:{0}\n\nПоказаны три последних обращения!",
    "en": "📜 Your requests:{0}\n\nOnly last three requests shown!",
}
sent_request_text: dict[str, str] = {
    "ru": """
    
<strong>Обращение #{0} ({1}):</strong>
Тема: {2}""",
    "en": """
    
<strong>Request #{0} ({1}):</strong>
Topic: {2}""",
}

button_text_back_to_topic: dict[str, tuple[str, str]] = {
    "ru": ("Вернуться к выбору типа обращений🔙", "bck_to_tpc"),
    "en": ("Back to the request type menu🔙", "bck_to_tpc"),
}

write_campus_or_dormitory_text: dict[str, str] = {
    "ru": "❔По поводу какого корпуса или общежития обращение? Напиши в чате полный адрес",
    "en": "❔What is your request about? Write the full address in the chat",
}

choose_faculty_text: dict[str, str] = {
    "ru": "❔С каким факультетом связано обращение?",
    "en": "❔What faculty is your request about?",
}

button_text_faculties: dict[str, list[tuple[str, str]]] = {
    "ru": [
        ("🧬Школа физико-математических и компьютерных наук", "cf_spmcs"),
        ("💰Школа экономики и менеджмента", "cf_sem"),
        ("👥Школа социальных наук", "cf_sss"),
        ("🎭Школа гуманитарных наук и искусств", "cf_sgas"),
        ("🗺Институт востоковедения и африканистики", "cf_iva"),
        ("🎨Школа дизайна", "cf_sd"),
        ("👨‍⚖️Юридический факультет", "cf_law"),
        ("🎒Факультет довузовского образования", "cf_pie"),
        button_text_back_to_topic["ru"],
    ],
    "en": [
        ("🧬School of Physics, Mathematics, and Computer Science", "cf_spmcs"),
        ("💰School of Economics and Management", "cf_sem"),
        ("👥School of Social Sciences", "cf_sss"),
        ("🎭School of Humanities and Arts", "cf_sgas"),
        ("🗺Institute of Oriental and African Studies", "cf_iva"),
        ("🎨School of Design", "cf_sd"),
        ("👨‍⚖️Faculty of Law", "cf_law"),
        ("🎒Pre-university Education Faculty", "cf_pie"),
        button_text_back_to_topic["en"],
    ],
}
button_text_faculties_ids: dict[str, int] = {
    key: i for i, (_, key) in enumerate(button_text_faculties["ru"])
}

choose_course_text: dict[str, str] = {
    "ru": "❔С каким курсом связано обращение?",
    "en": "❔What course is your request about?",
}

button_text_back_to_faculty: dict[str, tuple[str, str]] = {
    "ru": ("Вернуться к выбору факультета обращения🔙", "bck_to_fac"),
    "en": ("Back to the faculty selection menu🔙", "bck_to_fac"),
}
course_selection_callback_prefix: str = "cr_slc_"
button_text_courses: dict[str, list[tuple[str, str]]] = {
    "ru": [
        ("1️⃣Первый курс", course_selection_callback_prefix + "1"),
        ("2️⃣Второй курс", course_selection_callback_prefix + "2"),
        ("3️⃣Третий курс", course_selection_callback_prefix + "3"),
        ("4️⃣Четвёртый курс", course_selection_callback_prefix + "4"),
        ("5️⃣Пятый курс", course_selection_callback_prefix + "5"),
        (
            "🔄 Магистратура/Аспирантура/Другое",
            course_selection_callback_prefix + "mpo",
        ),
        button_text_back_to_faculty["ru"],
    ],
    "en": [
        ("1️⃣First year", course_selection_callback_prefix + "1"),
        ("2️⃣Second year", course_selection_callback_prefix + "2"),
        ("3️⃣Third year", course_selection_callback_prefix + "3"),
        ("4️⃣Fourth year", course_selection_callback_prefix + "4"),
        ("5️⃣Fifth year", course_selection_callback_prefix + "5"),
        ("🔄 Master's/PhD/Other", course_selection_callback_prefix + "mpo"),
        button_text_back_to_faculty["en"],
    ],
}
button_text_courses_ids: dict[str, int] = {
    key: i for i, (_, key) in enumerate(button_text_courses["ru"])
}

request_full_descr_text: dict[str, str] = {
    "ru": """📝 Пожалуйста, максимально подробно опиши подробности своего обращения. Все делегаты и волонтёры Студсовета подписали Соглашение о Неразглашении и гарантируют твою <strong>анонимность</strong> (если ты укажешь о ней в твоём обращении).

<strong>Важно!</strong> Прикладывай ссылки на подтверждающие описываемую ситуацию материалы (опросы, фото, видео, точные даты и время). Конкретика позволит нам решить твой запрос максимально эффективно. Загрузить всё можно для удобства на <a href=\"https://disk.yandex.ru/client/disk\">одну папку в облаке</a>, не забыв открыть доступ по ссылке.""",
    "en": """📝 Please, describe your problem in detail. If you wish to remain anonymous, state it in the body of your request. Don't worry, no-one will disclose information about you and your request since all the delegates and volunteers have signed the Non-Disclosure Agreement.

<strong>Note!</strong> We need you to attach materials (precise date when smth happened, photos, videos, polls etc.) that will help us with solving your problem. For convenience, create a folder using Google or Yandex drive and upload all of your files to it. Please, don't forget to make your folder accessible by link.""",
}

confirm_application_text: dict[str, str] = {
    "ru": """👀 Проверь, пожалуйста, корректность данных и наличие доступа по ссылке к прикреплённым материалам. Обращение в Студсовет будет отправлено в следующем виде:

————
{0}
————""",
    "en": """👀 Please check the correctness of the data and the availability of access via the link to your attached materials. The appeal to the Student Council will be sent in the following form:

————
{0}
————""",
}

campus_or_dormitory_text: dict[str, str] = {
    "ru": "\nОбщежитие или корпус ВШЭ: ",
    "en": "\nHSE dormitory or campus: ",
}

faculty: dict[str, str] = {
    "ru": "\nФакультет: ",
    "en": "\nFaculty: ",
}

course: dict[str, str] = {
    "ru": "\nКурс: ",
    "en": "\nCourse: ",
}

application_sent_text: dict[str, str] = {
    "ru": """<strong>Обращение от {user_name} (@{user_nick} | id={user_id}):</strong>

<strong>Тема: {topic}{second_row}{third_row}</strong>

{text}""",
    "en": """<strong>Application from {user_name} (@{user_nick} | id={user_id}):</strong>

<strong>Topic: {topic}{second_row}{third_row}</strong>

{text}""",
}

button_text_back_to_application: dict[str, tuple[str, str]] = {
    "ru": ("Вернуться к составлению текста обращения🔙", "bck_to_apl_wrt"),
    "en": ("Back to the application text menu🔙", "bck_to_apl_wrt"),
}
button_text_approve_application: dict[str, tuple[str, str]] = {
    "ru": ("Отправить обращение✅", "snd_appl"),
    "en": ("Send application✅", "snd_appl"),
}

wait_a_little_text: dict[str, str] = {
    "ru": "Подожди немного, прежде чем отправить новый запрос",
    "en": "Wait a little before sending a new request",
}

reqest_registred_text: dict[str, str] = {
    "ru": """🎉 Готово! Твой номер обращения:
{0}

Студсовет рассмотрит обращение и свяжется с вами в течение рабочей недели.""",
    "en": """🎉 Done! Your application number:
{0}

The Student Council will consider the application and contact you within a working week.""",
}

unknown_user_text = "Errror: user is unknown"
unexpected_error_text = "Unexpected error"
