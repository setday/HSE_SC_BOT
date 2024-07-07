block_enter_text: dict[str, str] = {
    "ru": """🤩 Мы открыты к сотрудничеству со Студенческими Организациями, клубами и прочими заинтересованными в нашей деятельности лицам!

📝 Пожалуйста, опишите ваше предложение максимально подробно. Прикладывайте ссылки на все материалы (опросы, фото, видео, точные даты и время). Конкретика позволяет нам решить решить вашу запрос максимально эффективно. Загрузить всё можно для удобства на <a href=\"https://disk.yandex.ru/client/disk\">одну папку в облаке</a>, не забыв открыть доступ по ссылке.""",
    "en": """🤩 We are open to cooperation with Student Organizations, clubs and other interested parties!

📝 Please describe your proposal in as much detail as possible. Attach links to all materials (surveys, photos, videos, exact dates and times). Specificity allows us to solve your request as efficiently as possible. You can upload everything for convenience to <a href=\"https://disk.yandex.ru/client/disk\">one folder in the cloud</a>, don't forget to open access via the link.""",
}
block_default_text = "Unknown text"

confirm_application_text: dict[str, str] = {
    "ru": """👀 Проверьте, пожалуйста, корректность данных и наличие доступа по ссылке к вашим прикреплённым материалам. Обращение в Студсовет будет отправлено в следующем виде:

————
<strong>Обращение от {0} (@{1}):</strong>

<strong>Тема: Сотрудничество</strong>

{2}
————""",
    "en": """👀 Please check the correctness of the data and the availability of access via the link to your attached materials. The appeal to the Student Council will be sent in the following form:

————
<strong>Appeal from {0} (@{1}):</strong>

<strong>Subject: Cooperation</strong>

{2}
————""",
}

application_sent_text: str = """<strong>Обращение от {0} (@{1}):</strong>

<strong>Тема: Сотрудничество</strong>

{2}"""

button_text_back_to_application: dict[str, tuple[str, str]] = {
    "ru": ("Вернуться в меню составления текста обращения🔙", "bck_to_prv_stg"),
    "en": ("Back to the application text menu🔙", "bck_to_prv_stg"),
}
button_text_approve_application: dict[str, tuple[str, str]] = {
    "ru": ("Отправить обращение✅", "snd_appl"),
    "en": ("Send application✅", "snd_appl"),
}

reqest_registred_text: dict[str, str] = {
    "ru": """🎉 Готово! Ваш номер обращения:
{0}

Студсовет рассмотрит обращение и свяжется с вами в течение рабочей недели.""",
    "en": """🎉 Done! Your application number:
{0}

The Student Council will consider the application and contact you within a working week.""",
}

unknown_user_text = "Errror: user is unknown"
