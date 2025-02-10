block_enter_text: dict[str, str] = {
    "ru": """🤩 Мы открыты к сотрудничеству со Студенческими Организациями, клубами и прочими заинтересованными в нашей деятельности лицами!

📝 Пожалуйста, опишите ваше предложение максимально подробно. Прикладывайте ссылки на все материалы (опросы, фото, видео, точные даты и время). Конкретика позволит нам решить ваш запрос максимально эффективно. Загрузить всё можно для удобства на <a href=\"https://disk.yandex.ru/client/disk\">одну папку в облаке</a>, не забыв открыть доступ по ссылке.""",
    "en": """🤩 We are open to cooperation with Student Organizations, clubs and other interested parties!

📝 Please describe your proposal in as much detail as possible. Attach links to all materials (surveys, photos, videos, exact dates and times). Specificity allows us to solve your request as efficiently as possible. You can upload everything for convenience to <a href=\"https://disk.yandex.ru/client/disk\">one folder in the cloud</a>, don't forget to open access via the link.""",
}

application_sent_text: dict[str, str] = {
    "ru": """<strong>Обращение от {user_name} (@{user_nick} | id={user_id}):</strong>

<strong>Тема: Сотрудничество</strong>

{request_text}""",
    "en": """<strong>Application from {user_name} (@{user_nick} | id={user_id}):</strong>

<strong>Topic: Cooperation</strong>
    
{request_text}""",
}

confirm_application_text: dict[str, str] = {
    "ru": """👀 Проверьте, пожалуйста, корректность данных и наличие доступа по ссылке к вашим прикреплённым материалам. Обращение в Студсовет будет отправлено в следующем виде:

————
{0}
————""".format(
        application_sent_text["ru"]
    ),
    "en": """👀 Please check the correctness of the data and the availability of access via the link to your attached materials. The appeal to the Student Council will be sent in the following form:

————
{0}
————""".format(
        application_sent_text["en"]
    ),
}

button_text_back_to_application: dict[str, str] = {
    "ru": "Вернуться в меню составления текста обращения🔙",
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
    "ru": """🎉 Готово! Ваш номер обращения:
{request_id}

Студсовет рассмотрит обращение и свяжется с вами в течение рабочей недели.""",
    "en": """🎉 Done! Your application number:
{request_id}

The Student Council will consider the application and contact you within a working week.""",
}
