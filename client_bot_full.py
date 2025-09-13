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
    telegram_id INTEGER UNIQUE,
    name TEXT,
    phone TEXT,
    comment TEXT,
    viewed INTEGER DEFAULT 0
)
""")
conn.commit()

# === КЛИЕНТСКОЕ МЕНЮ ===
client_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📌 Оставить заявку")],
        [KeyboardButton(text="ℹ️ О нас"), KeyboardButton(text="📞 Связаться")]
    ],
    resize_keyboard=True
)

# === КНОПКА «ГЛАВНОЕ МЕНЮ» ===
main_menu_button = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="🏠 Главное меню")]],
    resize_keyboard=True
)

# === АДМИН-МЕНЮ ===
admin_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📋 Новые заявки")],
        [KeyboardButton(text="📂 Все заявки")],
        [KeyboardButton(text="🗑️ Удалить заявку")]
    ],
    resize_keyboard=True
)

# === СТАРТ ===
@dp.message(Command("start"))
async def start(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        await message.answer("👨‍💼 Админ-панель", reply_markup=admin_keyboard)
    else:
        await message.answer("Добро пожаловать! Выберите действие:", reply_markup=client_keyboard)

# === ВОЗВРАТ В МЕНЮ ===
@dp.message(lambda m: m.text == "🏠 Главное меню")
async def back_to_main(message: types.Message):
    await message.answer("Вы вернулись в главное меню:", reply_markup=client_keyboard)

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
        "INSERT INTO clients (telegram_id, name, phone, comment) VALUES (?, ?, ?, ?)",
        (user_id, name, phone, comment)
    )
    conn.commit()

    # Уведомление админу
    await bot.send_message(
        ADMIN_ID,
        f"📩 Новая заявка:\n\nИмя: {name}\nТелефон: {phone}\nКомментарий: {comment}"
    )
    await message.answer("✅ Спасибо! Ваша заявка принята.", reply_markup=main_menu_button)
    del user_data[user_id]

# === ПРОЧИЕ КНОПКИ ===
@dp.message(lambda m: m.text == "ℹ️ О нас")
async def about(message: types.Message):
    await message.answer("Мы команда, которая работает с клиентами через Telegram-бота 🚀", reply_markup=main_menu_button)

@dp.message(lambda m: m.text == "📞 Связаться")
async def contact(message: types.Message):
    await message.answer("Связаться можно по телефону: +82-10-1234-5678", reply_markup=main_menu_button)

# === АДМИН-ФУНКЦИИ ===
@dp.message(lambda m: m.text == "📋 Новые заявки")
async def new_requests(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return
    cursor.execute("SELECT * FROM clients WHERE viewed = 0")
    rows = cursor.fetchall()
    if not rows:
        await message.answer("❌ Нет новых заявок.", reply_markup=admin_keyboard)
        return

    msg = "📋 Новые заявки:\n\n"
    for row in rows:
        client_id_db = row[0]
        telegram_id = row[1]
        msg += f"#{client_id_db} — {row[2]}, {row[3]}\nКомментарий: {row[4]}\n\n"

        # Уведомление клиенту о просмотре
        await bot.send_message(
            chat_id=telegram_id,
            text="✅ Ваша заявка просмотрена! Мы скоро с вами свяжемся."
        )

    await message.answer(msg, reply_markup=admin_keyboard)
    cursor.execute("UPDATE clients SET viewed = 1 WHERE viewed = 0")
    conn.commit()

@dp.message(lambda m: m.text == "📂 Все заявки")
async def all_requests(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return
    cursor.execute("SELECT * FROM clients")
    rows = cursor.fetchall()
    if not rows:
        await message.answer("❌ Нет заявок.", reply_markup=admin_keyboard)
        return
    msg = "📂 Все заявки:\n\n"
    for row in rows:
        msg += f"#{row[0]} — {row[2]}, {row[3]}\nКомментарий: {row[4]}\nПросмотрено: {'Да' if row[5] else 'Нет'}\n\n"
    await message.answer(msg, reply_markup=admin_keyboard)

@dp.message(lambda m: m.text == "🗑️ Удалить заявку")
async def delete_prompt(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return
    await message.answer("Введите ID заявки для удаления:\nПример: 3")

@dp.message(lambda m: m.text.isdigit() and m.from_user.id == ADMIN_ID)
async def delete_request(message: types.Message):
    client_id = int(message.text)
    cursor.execute("SELECT * FROM clients WHERE id = ?", (client_id,))
    if not cursor.fetchone():
        await message.answer(f"❌ Заявка #{client_id} не найдена.", reply_markup=admin_keyboard)
        return
    cursor.execute("DELETE FROM clients WHERE id = ?", (client_id,))
    conn.commit()
    await message.answer(f"✅ Заявка #{client_id} удалена.", reply_markup=admin_keyboard)

# === ЗАПУСК ===
async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
