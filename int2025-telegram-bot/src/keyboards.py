from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


# Главное меню (видно всегда снизу)
def main_menu():
    """
    Главное меню с кнопками для пользователя.
    Кнопка 'Мои подписки' отправляет команду /myreminders.
    Кнопка 'Очистить подписки' отправляет команду /clearreminders.
    """
    keyboard = [
        [KeyboardButton(text="📅 Матчи TI2025")],
        [KeyboardButton(text="🔔 Мои подписки", callback_data=None)],
        [KeyboardButton(text="Очистить подписки", callback_data=None)],
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


# Inline-кнопки для матчей
def matches_keyboard(matches: list):
    """
    Формирует inline-клавиатуру для списка матчей.
    Текст кнопки содержит команды, callback_data — только номер и время матча.
    """
    keyboard = []
    for i, match in enumerate(matches, start=1):
        btn = InlineKeyboardButton(
            text=f"🔔 Напомнить: {match['team1']} vs {match['team2']}",
            callback_data=f"notify_{i}_{match['time']}"
        )
        keyboard.append([btn])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
