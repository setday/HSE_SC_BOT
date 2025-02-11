from Utils.DefaultTexts import button_text_back_to_main_menu

something_went_wrong_text: dict[str, str] = {
    "ru": "❔Что-то пошло не так. Попробуй вернуться в главное меню и попробовать снова.",
    "en": "❔Something went wrong. Try to go back to the main menu and try again.",
}

block_enter_text: dict[str, str] = {
    "ru": "❔По какому поводу обращение?",
    "en": "❔What is your request about?",
}

button_your_requests_text: dict[str, str] = {
    "ru": "Твои обращения 👀",
    "en": "Your requests 👀",
}
topic_button_textes: list[tuple[dict[str, str], str]] = [
    ({"ru": "Присутствие Студсовета на апелляционной комиссии ☎️", "en": "Student Council presence at the appeals commission ☎️"}, "ct_app_com"),
    ({"ru": "Общежития или корпуса ВШЭ 🏡", "en": "Dormitory or HSE campus 🏡"}, "ct_cmp_or_drm_prb"),
    ({"ru": "Образовательный процесс 📖", "en": "Educational process 📖"}, "ct_edu_prb"),
    ({"ru": "Другое 💊", "en": "Other 💊"}, "ct_another_prb"),
]
button_text_topics_ids: dict[str, int] = {
    key: i for i, (_, key) in enumerate(topic_button_textes)
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

button_text_back_to_topic: dict[str, str] = {
    "ru": "Вернуться к выбору типа обращений🔙",
    "en": "Back to the request type menu🔙",
}

write_campus_or_dormitory_text: dict[str, str] = {
    "ru": "❔По поводу какого корпуса или общежития обращение? Напиши в чате полный адрес",
    "en": "❔What is your request about? Write the full address in the chat",
}

choose_faculty_text: dict[str, str] = {
    "ru": "❔С каким факультетом связано обращение?",
    "en": "❔What faculty is your request about?",
}

faculty_button_textes: list[tuple[dict[str, str], str]] = [
    ({"ru": "🧬Школа физико-математических и компьютерных наук", "en": "🧬School of Physics, Mathematics, and Computer Science"}, "cf_spmcs"),
    ({"ru": "💰Школа экономики и менеджмента", "en": "💰School of Economics and Management"}, "cf_sem"),
    ({"ru": "👥Школа социальных наук", "en": "👥School of Social Sciences"}, "cf_sss"),
    ({"ru": "🎭Школа гуманитарных наук и искусств", "en": "🎭School of Humanities and Arts"}, "cf_sgas"),
    ({"ru": "🗺Институт востоковедения и африканистики", "en": "🗺Institute of Oriental and African Studies"}, "cf_iva"),
    ({"ru": "🎨Школа дизайна", "en": "🎨School of Design"}, "cf_sd"),
    ({"ru": "👨‍⚖️Юридический факультет", "en": "👨‍⚖️Faculty of Law"}, "cf_law"),
    ({"ru": "🎒Факультет довузовского образования", "en": "🎒Pre-university Education Faculty"}, "cf_pie"),
]
button_text_faculties_ids: dict[str, int] = {
    key: i for i, (_, key) in enumerate(faculty_button_textes)
}

choose_course_text: dict[str, str] = {
    "ru": "❔С каким курсом связано обращение?",
    "en": "❔What course is your request about?",
}

button_text_back_to_faculty: dict[str, str] = {
    "ru": "Вернуться к выбору факультета обращения🔙",
    "en": "Back to the faculty selection menu🔙",
}
course_selection_callback_prefix: str = "cr_slc_"
course_button_textes: list[tuple[dict[str, str], str]] = [
    ({"ru": "1️⃣Первый курс", "en": "1️⃣First year"}, course_selection_callback_prefix + "1"),
    ({"ru": "2️⃣Второй курс", "en": "2️⃣Second year"}, course_selection_callback_prefix + "2"),
    ({"ru": "3️⃣Третий курс", "en": "3️⃣Third year"}, course_selection_callback_prefix + "3"),
    ({"ru": "4️⃣Четвёртый курс", "en": "4️⃣Fourth year"}, course_selection_callback_prefix + "4"),
    ({"ru": "5️⃣Пятый курс", "en": "5️⃣Fifth year"}, course_selection_callback_prefix + "5"),
    ({"ru": "🔄 Магистратура/Аспирантура/Другое", "en": "🔄 Master's/PhD/Other"}, course_selection_callback_prefix + "mpo"),
]
button_text_courses_ids: dict[str, int] = {
    key: i for i, (_, key) in enumerate(course_button_textes)
}

request_full_descr_text: dict[str, str] = {
    "ru": """📝 Пожалуйста, максимально подробно опиши подробности своего обращения. Все делегаты и волонтёры Студсовета подписали Соглашение о Неразглашении и гарантируют твою <strong>анонимность</strong> (если ты укажешь о ней в твоём обращении).

<strong>Важно!</strong> Прикладывай ссылки на подтверждающие описываемую ситуацию материалы (опросы, фото, видео, точные даты и время). Конкретика позволит нам решить твой запрос максимально эффективно. Загрузить всё можно для удобства на <a href=\"https://disk.yandex.ru/client/disk\">одну папку в облаке</a>, не забыв открыть доступ по ссылке.""",
    "en": """📝 Please, describe your problem in detail. If you wish to remain anonymous, state it in the body of your request. Don't worry, no-one will disclose information about you and your request since all the delegates and volunteers have signed the Non-Disclosure Agreement.

<strong>Note!</strong> We need you to attach materials (precise date when smth happened, photos, videos, polls etc.) that will help us with solving your problem. For convenience, create a folder using Google or Yandex drive and upload all of your files to it. Please, don't forget to make your folder accessible by link.""",
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

{request_text}""",
    "en": """<strong>Application from {user_name} (@{user_nick} | id={user_id}):</strong>

<strong>Topic: {topic}{second_row}{third_row}</strong>

{request_text}""",
}

confirm_application_text: dict[str, str] = {
    "ru": """👀 Проверь, пожалуйста, корректность данных и наличие доступа по ссылке к прикреплённым материалам. Обращение в Студсовет будет отправлено в следующем виде:

————
{request}
————""",
    "en": """👀 Please check the correctness of the data and the availability of access via the link to your attached materials. The appeal to the Student Council will be sent in the following form:

————
{request}
————""",
}

button_text_back_to_application: dict[str, str] = {
    "ru": "Вернуться к составлению текста обращения🔙",
    "en": "Back to the application text menu🔙",
}
button_text_approve_application: dict[str, str] = {
    "ru": "Отправить обращение✅",
    "en": "Send application✅",
}

wait_a_little_text: dict[str, str] = {
    "ru": "Подожди немного, прежде чем отправить новый запрос",
    "en": "Wait a little before sending a new request",
}

reqest_registred_text: dict[str, str] = {
    "ru": """🎉 Готово! Твой номер обращения:
{request_id}

Студсовет рассмотрит обращение и свяжется с вами в течение рабочей недели.""",
    "en": """🎉 Done! Your application number:
{request_id}

The Student Council will consider the application and contact you within a working week.""",
}

unknown_user_text = "Errror: user is unknown"
unexpected_error_text = "Unexpected error"
