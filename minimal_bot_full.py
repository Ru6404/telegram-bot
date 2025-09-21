import os
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler
import logging

# Логирование
logging.basicConfig(level=logging.INFO)

# Токен из env
TOKEN = os.getenv("TELEGRAM_TOKEN")
if not TOKEN:
    print("Ошибка: переменная окружения TELEGRAM_TOKEN не найдена!")
    exit(1)

# URL сайта (API)
SITE_URL = "http://localhost:8000"

# --- Команда /start ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Клиенты", callback_data='clients')],
        [InlineKeyboardButton("Заявки", callback_data='requests')],
        [InlineKeyboardButton("Статистика", callback_data='stats')],
        [InlineKeyboardButton("Помощь", callback_data='help')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Выберите действие:", reply_markup=reply_markup)

# --- Обработка кнопок ---
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == 'clients':
        # Пример запроса к API сайта
        try:
            response = requests.get(f"{SITE_URL}/api/clients")
            data = response.json()
            text = "\n".join([f"{c['id']}: {c['name']}" for c in data])
        except Exception as e:
            text = f"Не удалось получить клиентов: {e}"
        await query.edit_message_text(f"Список клиентов:\n{text}")
    
    elif query.data == 'requests':
        try:
            response = requests.get(f"{SITE_URL}/api/requests")
            data = response.json()
            text = "\n".join([f"{r['id']}: {r['title']}" for r in data])
        except Exception as e:
            text = f"Не удалось получить заявки: {e}"
        await query.edit_message_text(f"Заявки:\n{text}")
    
    elif query.data == 'stats':
        try:
            response = requests.get(f"{SITE_URL}/api/stats")
            data = response.json()
            text = "\n".join([f"{k}: {v}" for k, v in data.items()])
        except Exception as e:
            text = f"Не удалось получить статистику: {e}"
        await query.edit_message_text(f"Статистика:\n{text}")
    
    elif query.data == 'help':
        await query.edit_message_text("Помощь:\n- Клиенты: список клиентов\n- Заявки: заявки клиентов\n- Статистика: показатели работы\n- Помощь: эта справка")

# --- Лог всех сообщений (для отладки) ---
async def log_all_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        print("Сообщение от", update.message.from_user.username, ":", update.message.text)

# --- Создание приложения ---
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))
app.add_handler(CommandHandler("help", start))
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("stats", start))
app.add_handler(CommandHandler("requests", start))
app.add_handler(CommandHandler("clients", start))

# Лог всех сообщений
from telegram.ext import MessageHandler, filters
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, log_all_messages))

print("Бот запущен...")
app.run_polling()
