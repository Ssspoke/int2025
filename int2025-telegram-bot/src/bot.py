import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
from handlers import match_handlers

load_dotenv()

API_TOKEN = os.getenv("TOKEN")

async def main():
    if not API_TOKEN:
        print("Ошибка: не найден токен Telegram. Укажите его в .env как TOKEN=...")
        return
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(match_handlers.router)
    print("Bot is online!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())