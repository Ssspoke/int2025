import sqlite3
from datetime import datetime
from typing import List, Tuple

DB_PATH = 'src/utils/reminders.db'

# Создание таблицы, если не существует
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            match_id TEXT NOT NULL,
            match_time TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Добавить напоминание
# match_time — строка в формате ISO (например, '2025-09-11T10:00:00')
def add_reminder(user_id: int, match_id: str, match_time: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('INSERT INTO reminders (user_id, match_id, match_time) VALUES (?, ?, ?)',
              (user_id, match_id, match_time))
    conn.commit()
    conn.close()

# Получить все напоминания
# Возвращает список кортежей (id, user_id, match_id, match_time)
def get_all_reminders() -> List[Tuple]:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM reminders')
    rows = c.fetchall()
    conn.close()
    return rows

# Удалить напоминание по id
def delete_reminder(reminder_id: int):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('DELETE FROM reminders WHERE id = ?', (reminder_id,))
    conn.commit()
    conn.close()

# Получить напоминания для пользователя
def get_user_reminders(user_id: int) -> List[Tuple]:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM reminders WHERE user_id = ?', (user_id,))
    rows = c.fetchall()
    conn.close()
    return rows

# Вызвать при старте бота для инициализации БД
init_db()
