from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from services.liquipedia_parser import LiquipediaParser

router = Router()

@router.message(Command("start"))
async def start_command(message: Message):
    await message.answer(
        "Добро пожаловать! Я бот для отслеживания матчей The International 2025.\n"
        "Используйте команду /matches, чтобы получить информацию о текущих матчах."
    )

MAX_MESSAGE_LENGTH = 4096

def split_message(text, max_length=MAX_MESSAGE_LENGTH):
    # Разбивает текст на части не длиннее max_length
    return [text[i:i+max_length] for i in range(0, len(text), max_length)]

@router.message(Command("matches"))
async def matches_command(message: Message):
    parser = LiquipediaParser()
    matches = parser.fetch_matches()
    if not matches:
        await message.answer("Не удалось получить данные о матчах. Попробуйте позже.")
        return
    text = "Текущие матчи The International 2025:\n\n"
    for match in matches:
        text += f"{match['team1']} vs {match['team2']} | Время: {match['time']} | Статус: {match['status']}\n"
    for part in split_message(text):
        await message.answer(part)