block_enter_text = "Какова тема обращения обращение?"
detailed_text = "Понял. Теперь можешь описать подробнее?"

button_option_edu = "Проблема в образовательном процессе"
button_option_support = "Присутствие Студсовета на аппеляционной комиссии"
button_option_campus = "Проблема в корпусах"
button_option_dormitory = "Проблема с общежитиями"
button_option_another = "Другое"

faculty_question_text = "Укажи пожалуйста свой факультет и курс"

block_default_text = "Мы примим заявку в следующем виде:"

reqest_registred_text = "Будем решать данный вопрос!"

unknown_user = "Errror: user is unknown"

def recover_option_text(text: str) -> str:
    if text == button_option_edu[:30]:
        return button_option_edu
    if text == button_option_support[:30]:
        return button_option_support
    return text
