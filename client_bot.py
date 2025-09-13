import sqlite3
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

# === КОНФИГ ===
API_TOKEN = "8253068855:AAFPNJke9PYju90RgZe4ZOKOuuMSJNAs0X8"
ADMIN_ID = 5569793273

# === ИНИЦИАЛИЗАЦИЯ ===
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# === БАЗА ДАННЫХ ===
conn = sqlite3.connect("clients.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS clients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    phone TEXT,
    comment TEXT
)
""")
conn.commit()

# === СТАРТ ===
@dp.message(Command("start"))
async def start(message: types.Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📌 Оставить заявку")],
            [KeyboardButton(text="ℹ️ О нас"), KeyboardButton(text="📞 Связаться")]
        ],
        resize_keyboard=True
    )
    await message.answer("Добро пожаловать! Выберите действие:", reply_markup=keyboard)

# === СОЗДАНИЕ ЗАЯВКИ ===
user_data = {}

@dp.message(lambda m: m.text == "📌 Оставить заявку")
async def get_name(message: types.Message):
    user_data[message.from_user.id] = {}
    await message.answer("Ruslan:")

@dp.message(lambda m: m.from_user.id in user_data and "name" not in user_data[m.from_user.id])
async def save_name(message: types.Message):
    user_data[message.from_user.id]["name"] = message.text
    await message.answer("+821021556564:")

@dp.message(lambda m: m.from_user.id in user_data and "phone" not in user_data[m.from_user.id])
async def save_phone(message: types.Message):
    user_data[message.from_user.id]["phone"] = message.text
    await message.answer("Введите комментарий:")

@dp.message(lambda m: m.from_user.id in user_data and "comment" not in user_data[m.from_user.id])
async def save_comment(message: types.Message):
    user_id = message.from_user.id
    name = user_data[user_id]["name"]
    phone = user_data[user_id]["phone"]
    comment = message.text

    cursor.execute(
        "INSERT INTO clients (name, phone, comment) VALUES (?, ?, ?)",
        (name, phone, comment)
    )
    conn.commit()

    # Уведомление админу
    await bot.send_message(
        ADMIN_ID,
        f"📩 Новая заявка:\n\nИмя: {name}\nТелефон: {phone}\nКомментарий: {comment}"
    )
    await message.answer("✅ Спасибо! Ваша заявка принята.")
    del user_data[user_id]

# === ПРОЧИЕ КНОПКИ ===
@dp.message(lambda m: m.text == "ℹ️ О нас")
async def about(message: types.Message):
    await message.answer("Мы команда, которая работает с клиентами через Telegram-бота 🚀")

@dp.message(lambda m: m.text == "📞 Связаться")
async def contact(message: types.Message):
    await message.answer("Связаться можно по телефону: +82-10-1234-5678")

# === АДМИН-ПАНЕЛЬ ===
@dp.message(Command("admin"))
async def admin_panel(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("⛔ У вас нет доступа.")
        return

    cursor.execute("SELECT * FROM clients")
    rows = cursor.fetchall()

    if not rows:
        await message.answer("❌ Пока нет заявок.")
        return

    msg = "📋 Список заявок:\n\n"
    for i, row in enumerate(rows, start=1):
        msg += f"#{row[0]} — {row[1]}, {row[2]}\nКомментарий: {row[3]}\n\n"

        # Отправка каждые 5 заявок, чтобы сообщение не было слишком длинным
        if i % 5 == 0:
            await message.answer(msg)
            msg = ""

    if msg:
        await message.answer(msg)

# === ЗАПУСК ===
async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
