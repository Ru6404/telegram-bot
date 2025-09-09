from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
import requests
import logging
from datetime import datetime
import json
import os
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Токен бота из .env файла
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

if not TOKEN:
    print("❌ ОШИБКА: Токен не найден!")
    exit(1)

class QuantumTelegramBot:
    def __init__(self):
        self.token = TOKEN
        print("✅ Токен загружен")
        self.app = Application.builder().token(self.token).build()
        self.setup_handlers()

    def setup_handlers(self):
        self.app.add_handler(CommandHandler("start", self.start))
        self.app.add_handler(CommandHandler("help", self.help_command))
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("🚀 Бот запущен!")

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("📋 Помощь: /start, /help")

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        text = update.message.text
        await update.message.reply_text(f"🔮 Вы сказали: {text}")

    def run(self):
        print("🤖 Бот запускается...")
        try:
            self.app.run_polling()
        except Exception as e:
            print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    bot = QuantumTelegramBot()
    bot.run()
