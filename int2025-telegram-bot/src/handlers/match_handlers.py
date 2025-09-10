from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from services.liquipedia_parser import LiquipediaParser
from keyboards import matches_keyboard
from utils.reminders_db import add_reminder, get_user_reminders

router = Router()

@router.message(Command("start"))
async def start_command(message: Message):
    await message.answer(
        "Добро пожаловать! Я бот для отслеживания матчей The International 2025.\n"
        "Используйте команду /matches, чтобы получить информацию о текущих матчах."
    )

MAX_MESSAGE_LENGTH = 4096

def split_message(text, max_length=MAX_MESSAGE_LENGTH):
    return [text[i:i+max_length] for i in range(0, len(text), max_length)]




@router.message(Command("matches"))
@router.message(F.text == "📅 Матчи TI2025")  # теперь доступно и из меню
async def matches_command(message: Message):
    parser = LiquipediaParser()
    matches = parser.fetch_matches(limit=5)
    if not matches:
        await message.answer("Не удалось получить данные о матчах. Попробуйте позже.")
        return

    text = "🎯 <b>Ближайшие матчи The International 2025:</b>\n\n"
    for i, match in enumerate(matches, start=1):
        text += (
            f"{i}. <b>{match['team1']} vs {match['team2']}</b>\n"
            f" 🕒{match['time']}\n"
            f" 📌{match['stage']}\n"
            f"📍 Статус: {match['status']}\n\n"
        )

    await message.answer(text, parse_mode="HTML", reply_markup=matches_keyboard(matches))


@router.callback_query(F.data.startswith("notify_"))
async def notify_match(callback: CallbackQuery):
    # Ожидаем callback.data в формате notify_{match_id}_{match_time}
    try:
        _, match_id, match_time = callback.data.split("_", 2)
        user_id = callback.from_user.id
        add_reminder(user_id, match_id, match_time)
        await callback.answer(f"🔔 Напоминание оформлено на матч №{match_id}!")
    except Exception as e:
        await callback.answer("Ошибка при оформлении напоминания.")

@router.message(Command("myreminders"))
@router.message(F.text == "Мои подписки")
async def my_reminders(message: Message):
    user_id = message.from_user.id
    reminders = get_user_reminders(user_id)
    if not reminders:
        await message.answer("У вас нет активных подписок на матчи.")
        return
    text = "<b>Ваши подписки на матчи:</b>\n\n"
    for r in reminders:
        # r = (id, user_id, match_id, match_time)
        text += f"Матч №{r[2]} в {r[3]}\n"
    await message.answer(text, parse_mode="HTML")
