import logging
import sqlite3
import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

API_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Клавиатура админа
admin_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton("📋 Новые заявки"), KeyboardButton("📂 Все заявки")],
        [KeyboardButton("➕ Добавить клиента"), KeyboardButton("✅ Принять заявку"), KeyboardButton("❌ Отклонить заявку")],
        [KeyboardButton("📊 Статистика")]
    ],
    resize_keyboard=True
)

# Клавиатура пользователя
user_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton("📌 Оставить заявку")],
        [KeyboardButton("ℹ️ О нас"), KeyboardButton("📞 Связаться")]
    ],
    resize_keyboard=True
)

# Инициализация базы данных
conn = sqlite3.connect("clients.db")
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS clients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    telegram_id INTEGER,
    name TEXT,
    username TEXT,
    phone TEXT,
    comment TEXT,
    status TEXT DEFAULT 'new',
    viewed INTEGER DEFAULT 0
)
''')
conn.commit()

# --- Команда /start ---
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        await message.answer("👨‍💼 Админ-панель", reply_markup=admin_keyboard)
    else:
        await message.answer("Добро пожаловать! Выберите действие:", reply_markup=user_keyboard)

# --- Пользователь оставляет заявку ---
@dp.message_handler(lambda m: m.text == "📌 Оставить заявку")
async def leave_request(message: types.Message):
    await message.answer("Напишите ваше имя:")

# --- Уведомления админа о новых заявках ---
async def notify_admin_new_requests():
    while True:
        cursor.execute('SELECT id, name FROM clients WHERE status="new" AND viewed=0')
        new_requests = cursor.fetchall()
        for req in new_requests:
            await bot.send_message(
                ADMIN_ID,
                f"📩 Новая заявка: #{req[0]} — {req[1]}"
            )
            cursor.execute('UPDATE clients SET viewed=1 WHERE id=?', (req[0],))
            conn.commit()
        await asyncio.sleep(60)

# --- Запуск ---
async def main():
    asyncio.create_task(notify_admin_new_requests())
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
