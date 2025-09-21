import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import logging

# Логирование
logging.basicConfig(level=logging.INFO)

# Берём токен из переменной окружения
TOKEN = os.getenv("TELEGRAM_TOKEN")

if not TOKEN:
    print("Ошибка: переменная окружения TELEGRAM_TOKEN не найдена!")
    exit(1)

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Бот активен ✅")

# Создание приложения и добавление обработчика команды /start
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))

# Запуск бота
print("Бот запущен...")
app.run_polling()
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import logging

# Логирование
logging.basicConfig(level=logging.INFO)

# Берём токен из переменной окружения
TOKEN = os.getenv("TELEGRAM_TOKEN")

if not TOKEN:
    print("Ошибка: переменная окружения TELEGRAM_TOKEN не найдена!")
    exit(1)

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Бот активен ✅")

# Создание приложения и добавление обработчика команды /start
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))

# Запуск бота
print("Бот запущен...")
app.run_polling()
