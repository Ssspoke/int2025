from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def matches_navigation():
    keyboard = [
        [
            InlineKeyboardButton(text="⬅️ Назад", callback_data="prev_matches"),
            InlineKeyboardButton(text="➡️ Вперёд", callback_data="next_matches"),
        ],
        [
            InlineKeyboardButton(text="🔄 Обновить", callback_data="refresh_matches"),
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def match_actions(match_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔔 Напомнить", callback_data=f"notify_{match_id}")]
        ]
    )

