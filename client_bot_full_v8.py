import logging
import sqlite3
import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher.filters import Text
from aiogram.utils.callback_data import CallbackData

API_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# --- Клавиатуры ---
admin_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton("📋 Новые заявки"), KeyboardButton("📂 Все заявки")],
        [KeyboardButton("📊 Статистика")]
    ],
    resize_keyboard=True
)

user_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton("📌 Оставить заявку")],
        [KeyboardButton("ℹ️ О нас"), KeyboardButton("📞 Связаться")]
    ],
    resize_keyboard=True
)

# --- CallbackData для кнопок ---
request_cb = CallbackData("request", "action", "client_id")

# --- База данных ---
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

# --- /start ---
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        await message.answer("👨‍💼 Админ-панель", reply_markup=admin_keyboard)
    else:
        await message.answer("Добро пожаловать! Выберите действие:", reply_markup=user_keyboard)

# --- Пользователь оставляет заявку ---
@dp.message_handler(Text("📌 Оставить заявку"))
async def leave_request(message: types.Message):
    await message.answer("Введите ваше имя:")

# --- Админ: новые заявки с кнопками ---
@dp.message_handler(Text("📋 Новые заявки"))
async def new_requests(message: types.Message):
    cursor.execute('SELECT id, name, username, phone FROM clients WHERE status="new"')
    rows = cursor.fetchall()
    if not rows:
        await message.answer("Нет новых заявок.", reply_markup=admin_keyboard)
        return
    for row in rows:
        client_id = row[0]
        text = f"📩 Заявка #{client_id}\nИмя: {row[1]}\nТелеграм: @{row[2]}\nТелефон: {row[3]}"
        markup = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton("✅ Принять", callback_data=request_cb.new(action="accept", client_id=client_id)),
             InlineKeyboardButton("❌ Отклонить", callback_data=request_cb.new(action="decline", client_id=client_id))]
        ])
        await message.answer(text, reply_markup=markup)

# --- Обработка кнопок принять/отклонить ---
@dp.callback_query_handler(request_cb.filter())
async def process_request(call: types.CallbackQuery, callback_data: dict):
    client_id = int(callback_data["client_id"])
    action = callback_data["action"]
    if action == "accept":
        cursor.execute('UPDATE clients SET status="accepted" WHERE id=?', (client_id,))
        conn.commit()
        await call.message.edit_text(f"✅ Заявка #{client_id} принята")
    elif action == "decline":
        cursor.execute('UPDATE clients SET status="declined" WHERE id=?', (client_id,))
        conn.commit()
        await call.message.edit_text(f"❌ Заявка #{client_id} отклонена")
    await call.answer()  # Убирает "часики" на кнопке

# --- Статистика ---
@dp.message_handler(Text("📊 Статистика"))
async def statistics(message: types.Message):
    cursor.execute('SELECT COUNT(*) FROM clients')
    total = cursor.fetchone()[0]
    cursor.execute('SELECT COUNT(*) FROM clients WHERE status="new"')
    new_count = cursor.fetchone()[0]
    cursor.execute('SELECT COUNT(*) FROM clients WHERE status="accepted"')
    accepted_count = cursor.fetchone()[0]
    cursor.execute('SELECT COUNT(*) FROM clients WHERE status="declined"')
    declined_count = cursor.fetchone()[0]
    text = f"""
📊 Статистика:
Всего заявок: {total}
Новые: {new_count}
Принятые: {accepted_count}
Отклоненные: {declined_count}
"""
    await message.answer(text, reply_markup=admin_keyboard)

# --- Уведомления админа о новых заявках ---
async def notify_admin_new_requests():
    while True:
        cursor.execute('SELECT id, name FROM clients WHERE status="new" AND viewed=0')
        new_requests = cursor.fetchall()
        for req in new_requests:
            markup = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton("✅ Принять", callback_data=request_cb.new(action="accept", client_id=req[0])),
                 InlineKeyboardButton("❌ Отклонить", callback_data=request_cb.new(action="decline", client_id=req[0]))]
            ])
            await bot.send_message(
                ADMIN_ID,
                f"📩 Новая заявка: #{req[0]} — {req[1]}",
                reply_markup=markup
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
