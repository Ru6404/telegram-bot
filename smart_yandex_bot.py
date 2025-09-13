from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
import logging
import sys
import os
import requests
import json

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from config import BOT_TOKEN, ADMIN_ID
except ImportError:
    print("❌ Ошибка: Проверьте config.py с BOT_TOKEN и ADMIN_ID!")
    sys.exit(1)

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

WAITING_QUESTION = 1

# Бесплатный Yandex GPT API
async def ask_yandex_gpt(question):
    try:
        # Используем открытый API (может потребовать VPN)
        url = "https://api.aimybox.com/chat"
        
        data = {
            "question": question,
            "bot_id": "general-assistant"
        }
        
        response = requests.post(url, json=data, timeout=15)
        
        if response.status_code == 200:
            result = response.json()
            return result.get('answer', 'Не удалось получить ответ')
        else:
            return "📡 Ошибка подключения к нейросети"
            
    except Exception as e:
        logger.error(f"Yandex GPT error: {e}")
        return "⚠️ Временные технические трудности"

# Функция старта
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    
    await update.message.reply_text(
        f"🤖 Привет, {user.first_name}!\n"
        "Я умный бот-помощник с нейросетью!\n"
        "Задайте мне любой вопрос:"
    )
    await show_main_menu(update)
    return ConversationHandler.END

async def show_main_menu(update: Update):
    keyboard = [
        ["🤖 Задать вопрос", "📊 Статус системы"],
        ["📋 Помощь", "🏠 Главное меню"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Выберите действие:", reply_markup=reply_markup)

async def start_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("💡 Задайте ваш вопрос нейросети:")
    return WAITING_QUESTION

async def handle_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    question = update.message.text
    await update.message.reply_text("🤔 Думаю...")
    
    response = await ask_yandex_gpt(question)
    await update.message.reply_text(f"💡 Нейросеть отвечает:\n\n{response}")
    
    await show_main_menu(update)
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Диалог отменен")
    await show_main_menu(update)
    return ConversationHandler.END

async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    if text == "📊 Статус системы":
        await update.message.reply_text("📊 Система работает стабильно! ✅")
    elif text == "📋 Помощь":
        await update.message.reply_text("📋 Задайте мне любой вопрос!")
    elif text == "🏠 Главное меню":
        await show_main_menu(update)

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    
    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("^🤖 Задать вопрос$"), start_question)],
        states={WAITING_QUESTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_question)]},
        fallbacks=[CommandHandler("cancel", cancel)]
    )
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(conv_handler)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_buttons))
    
    print("🤖 Бот с Yandex GPT запущен!")
    application.run_polling()

if __name__ == '__main__':
    main()
