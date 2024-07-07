cancel_text = "X Отмена"
canceled_text = "Отменено"
create_text = "+ Создать"
created_text = "✓ Создано"
send_text = "Отправить >"
sent_text = "✓ Отправлено"

done_text = "✓ Готово"

save_text = "Сохранить"
saved_text = "✓ Сохранено"
delete_text = "Удалить"
deleted_text = "X Удалено"
edit_text = "Изменить"
edited_text = "✓ Изменено"

yes_text = "Да"
no_text = "Нет"

next_text = "Далее >"
prev_text = "< Назад"

back_text = "< Назад"
back_to_menu_text = "< Назад в меню"

button_text_back_to_main_menu: dict[str, tuple[str, str]] = {
    "ru": ("Вернуться в главное меню🔙", "bck_to_mm"),
    "en": ("Back to main menu🔙", "bck_to_mm"),
}


async def get_lang_from_state(state: any) -> str:
    try:
        data = await state.get_data()
        lang = data["language"]
        if lang not in ["ru", "en"]:
            return "ru"
        return lang
    except:
        return "ru"
