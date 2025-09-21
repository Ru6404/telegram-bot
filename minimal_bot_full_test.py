import os
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
import logging

# Логирование
logging.basicConfig(level=logging.INFO)

# Токен из env
TOKEN = os.getenv("TELEGRAM_TOKEN")
if not TOKEN:
    print("Ошибка: переменная окружения TELEGRAM_TOKEN не найдена!")
    exit(1)

# --- Имитируем данные (для теста без сайта) ---
clients_data = [
    {"id": 1, "name": "Иван Иванов"},
    {"id": 2, "name": "Мария Петрова"},
    {"id": 3, "name": "Алексей Смирнов"}
]

requests_data = [
    {"id": 101, "title": "Заявка №1"},
    {"id": 102, "title": "Заявка №2"},
    {"id": 103, "title": "Заявка №3"}
]

stats_data = {
    "Клиенты": 3,
    "Заявки": 3,
    "Активных пользователей": 2
}

# --- Команда /start ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Убираем старые кнопки
    await update.message.reply_text("Бот активен ✅", reply_markup=ReplyKeyboardRemove())

    # Новые кнопки под чатом
    keyboard = [
        [KeyboardButton("Клиенты"), KeyboardButton("Заявки")],
        [KeyboardButton("Статистика"), KeyboardButton("Помощь")]
    ]
    reply_markup = ReplyKeyboardMarkup(
        keyboard, resize_keyboard=True, one_time_keyboard=False
    )
    await update.message.reply_text("Выберите действие:", reply_markup=reply_markup)

# --- Обработка сообщений кнопок ---
async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    print("Нажата кнопка:", text)  # Лог кнопок

    if text == "Клиенты":
        msg = "\n".join([f"{c['id']}: {c['name']}" for c in clients_data])
        await update.message.reply_text(f"Список клиентов:\n{msg}")

    elif text == "Заявки":
        msg = "\n".join([f"{r['id']}: {r['title']}" for r in requests_data])
        await update.message.reply_text(f"Заявки:\n{msg}")

    elif text == "Статистика":
        msg = "\n".join([f"{k}: {v}" for k, v in stats_data.items()])
        await update.message.reply_text(f"Статистика:\n{msg}")

    elif text == "Помощь":
        await update.message.reply_text(
            "Помощь:\n- Клиенты: список клиентов\n- Заявки: заявки клиентов\n- Статистика: показатели работы\n- Помощь: эта справка"
        )

# --- Лог всех сообщений ---
async def log_all_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        print("Сообщение:", update.message.text)

# --- Создание приложения ---
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_button))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, log_all_messages))

print("Бот запущен...")
app.run_polling()
