import os
import logging
import httpx
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes, CommandHandler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = "8253068855:AAFPNJke9PYju90RgZe4ZOKOuuMSJNAs0X8"
API_URL = "http://localhost:8000"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text
    message_lower = message.lower()
    
    # Приветствия
    if any(word in message_lower for word in ['привет', 'hello', 'hi', 'start']):
        await update.message.reply_text("👋 Привет! Я бот для Auto-Cloud системы! Напишите 'меню' для команд.")
        return
    
    # Меню
    elif any(word in message_lower for word in ['меню', 'menu', 'команды']):
        await update.message.reply_text(
            "📋 Команды:\n• пользователи\n• задачи\n• добавить пользователя Иван mail@mail.ru\n• добавить задачу Заголовок Описание\n• статус"
        )
        return
    
    # Статус
    elif 'статус' in message_lower:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{API_URL}/users")
                users = response.json() if response.status_code == 200 else []
                await update.message.reply_text(f"🏢 Система работает! Пользователей: {len(users)}")
        except:
            await update.message.reply_text("❌ API недоступен! Запустите: python main.py")
        return
    
    # Остальное
    else:
        await update.message.reply_text("❓ Напишите 'меню' для списка команд")

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    logger.info("Бот запущен...")
    application.run_polling()

if __name__ == "__main__":
    main()
