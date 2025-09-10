import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command
from dotenv import load_dotenv

from handlers import match_handlers
from keyboards import main_menu

load_dotenv()

API_TOKEN = os.getenv("TOKEN")


async def main():
    if not API_TOKEN:
        print("❌ Ошибка: не найден токен Telegram. Укажите его в .env как TOKEN=...")
        return

    bot = Bot(token=API_TOKEN, parse_mode="HTML")
    dp = Dispatcher(storage=MemoryStorage())

    # Регистрируем роутеры
    dp.include_router(match_handlers.router)

    # Хэндлер для команды /start
    @dp.message(Command("start"))
    async def start_cmd(message: Message):
        await message.answer(
            "👋 Привет! Я бот для отслеживания матчей The International 2025.\n\n"
            "Используй меню ниже для выбора:",
            reply_markup=main_menu()
        )

    print("✅ Bot is online!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
