from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


# Главное меню (видно всегда снизу)
def main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📅 Матчи TI2025")],
            [KeyboardButton(text="🔔 Мои подписки")],
            [KeyboardButton(text="ℹ️ Помощь")],
        ],
        resize_keyboard=True
    )


# Inline-кнопки для матчей
def matches_keyboard(matches: list):
    keyboard = []
    for i, match in enumerate(matches, start=1):
        keyboard.append([
            InlineKeyboardButton(
                text=f"🔔 Напомнить: {match['team1']} vs {match['team2']}",
                callback_data=f"notify_{i}"
            )
        ])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
