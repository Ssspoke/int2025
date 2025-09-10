from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from services.liquipedia_parser import LiquipediaParser
from keyboards import matches_keyboard

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
    match_id = callback.data.split("_")[1]
    # TODO: сохранять подписку в базу данных
    await callback.answer(f"🔔 Подписка оформлена на матч №{match_id}!")
