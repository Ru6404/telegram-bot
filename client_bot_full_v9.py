import asyncio
import logging
import os
from datetime import datetime, timedelta
import aiosqlite
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.filters import Text

# ------------------ Конфигурация ------------------
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ------------------ База данных ------------------
DB_PATH = "bot_database.db"

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE,
            username TEXT,
            first_name TEXT,
            last_name TEXT,
            phone TEXT,
            registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            message_count INTEGER DEFAULT 0,
            last_message_date TIMESTAMP
        )
        ''')
        await db.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER,
            title TEXT,
            description TEXT,
            status TEXT DEFAULT 'active',
            priority TEXT DEFAULT 'medium',
            created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        await db.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER,
            product_name TEXT,
            quantity INTEGER,
            price REAL,
            status TEXT DEFAULT 'new',
            created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        await db.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER,
            message_text TEXT,
            created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        await db.commit()

# ------------------ Клавиатуры ------------------
admin_markup = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton("📋 Новые заявки"), KeyboardButton("📂 Все заявки")],
        [KeyboardButton("👥 Клиенты"), KeyboardButton("📊 Статистика")],
        [KeyboardButton("📨 Рассылка"), KeyboardButton("⚙️ Настройки")],
        [KeyboardButton("Добавить клиента"), KeyboardButton("Принять"), KeyboardButton("Отказать")]
    ],
    resize_keyboard=True
)

client_markup = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton("📞 Связаться"), KeyboardButton("ℹ️ О нас")],
        [KeyboardButton("📌 Оставить заявку")]
    ],
    resize_keyboard=True
)

# ------------------ Инициализация бота ------------------
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# ------------------ Хэндлеры ------------------
@dp.message(Text(equals="/start"))
async def cmd_start(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        await message.answer("👨‍💼 Админ-панель\nВыберите действие:", reply_markup=admin_markup)
    else:
        await message.answer("Добро пожаловать! Выберите действие:", reply_markup=client_markup)

# ------------------ Обработка клиентов ------------------
@dp.message(Text(equals=["📌 Оставить заявку"]))
async def leave_request(message: types.Message):
    user = message.from_user
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT OR IGNORE INTO clients (user_id, username, first_name, last_name) VALUES (?, ?, ?, ?)",
            (user.id, user.username, user.first_name, user.last_name)
        )
        await db.commit()
    await message.answer("Ваша заявка принята! Ожидайте ответа.")

# ------------------ Админ: заявки ------------------
@dp.message(Text(equals=["📋 Новые заявки"]))
async def show_new_requests(message: types.Message):
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT id, first_name, last_name, username FROM clients ORDER BY registration_date DESC"
        )
        rows = await cursor.fetchall()
    if not rows:
        await message.answer("Новых заявок нет.")
        return
    text = "📋 <b>Новые заявки:</b>\n\n"
    for r in rows:
        text += f"#{r[0]} — {r[1]} {r[2]}, @{r[3]}\nКомментарий: None\nПросмотрено: Нет\n\n"
    await message.answer(text, parse_mode="HTML")

# ------------------ Админ: клиенты ------------------
@dp.message(Text(equals=["Добавить клиента"]))
async def add_client(message: types.Message):
    await message.answer("Введите user_id нового клиента:")
    # Для простоты можно добавить через последующий обработчик

@dp.message(Text(equals=["Принять"]))
async def accept_request(message: types.Message):
    await message.answer("Заявка принята ✅")

@dp.message(Text(equals=["Отказать"]))
async def reject_request(message: types.Message):
    await message.answer("Заявка отклонена ❌")

# ------------------ Рассылка ------------------
@dp.message(Text(equals=["📨 Рассылка"]))
async def broadcast_start(message: types.Message):
    await message.answer("Введите сообщение для рассылки:", reply_markup=ReplyKeyboardRemove())

@dp.message()
async def broadcast_send(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return
    text = message.text
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("SELECT user_id FROM clients WHERE user_id != ?", (ADMIN_ID,))
        clients = await cursor.fetchall()
    for c in clients:
        try:
            await bot.send_message(c[0], f"📢 <b>Рассылка:</b>\n{text}", parse_mode="HTML")
        except:
            pass
    await message.answer("✅ Рассылка завершена", reply_markup=admin_markup)

# ------------------ Запуск бота ------------------
async def main():
    await init_db()
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
