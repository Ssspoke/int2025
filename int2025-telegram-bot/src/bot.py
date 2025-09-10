import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command
from dotenv import load_dotenv
from handlers import match_handlers
from keyboards import main_menu
from utils.reminders_db import get_all_reminders, delete_reminder
from datetime import datetime, timedelta

load_dotenv()

API_TOKEN = os.getenv("TOKEN")

# Количество минут до матча для отправки уведомления (по умолчанию 10, для теста можно поставить 1)
REMINDER_MINUTES = int(os.getenv("TEST_REMINDER_MINUTES", 10))


async def reminder_worker(bot: Bot):
    """
    Фоновая задача: раз в минуту проверяет напоминания и отправляет уведомления пользователям,
    если до матча осталось <= REMINDER_MINUTES.
    После отправки напоминание удаляется из БД.
    """
    while True:
        now = datetime.now()
        reminders = get_all_reminders()
        for reminder in reminders:
            reminder_id, user_id, match_id, match_time = reminder
            try:
                match_dt = datetime.strptime(match_time.split('(')[0].strip(), '%d %B %Y, %H:%M')
            except Exception:
                try:
                    match_dt = datetime.strptime(match_time.split('(')[0].strip(), '%d.%m.%Y, %H:%M')
                except Exception:
                    continue
            delta = (match_dt - now).total_seconds() / 60
            if 0 <= delta <= REMINDER_MINUTES:
                try:
                    await bot.send_message(user_id, f"⏰ Напоминание! Матч №{match_id} начнётся в {match_time}")
                except Exception:
                    pass
                delete_reminder(reminder_id)
        await asyncio.sleep(60)


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
    # Запуск фоновой задачи для напоминаний
    asyncio.create_task(reminder_worker(bot))
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
