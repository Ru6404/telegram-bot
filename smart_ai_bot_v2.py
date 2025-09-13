from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
import logging
import sys
import os
import requests
import json

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from config import BOT_TOKEN, ADMIN_ID, OPENAI_API_KEY
except ImportError:
    print("❌ Ошибка: Проверьте config.py с BOT_TOKEN, ADMIN_ID и OPENAI_API_KEY!")
    sys.exit(1)

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Состояния для ConversationHandler
WAITING_QUESTION = 1

# Функция запроса к OpenAI
async def ask_ai(question):
    try:
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": question}],
            "temperature": 0.7
        }
        
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content']
        else:
            return "❌ Ошибка подключения к ИИ"
            
    except Exception as e:
        logger.error(f"AI error: {e}")
        return "⚠️ Произошла ошибка при обработке запроса"

# Функция старта
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    logger.info(f"User {user.first_name} started the bot")
    
    await update.message.reply_text(
        f"🤖 Привет, {user.first_name}!\n"
        "Я умный бот-помощник с искусственным интеллектом!\n"
        "Задайте мне любой вопрос или выберите действие:"
    )
    await show_main_menu(update)
    return ConversationHandler.END

# Показать главное меню
async def show_main_menu(update: Update):
    keyboard = [
        ["🤖 Задать вопрос ИИ", "📊 Статус системы"],
        ["📋 Помощь", "🏠 Главное меню"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Выберите действие:", reply_markup=reply_markup)

# Начать диалог с ИИ
async def start_ai_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("💡 Задайте ваш вопрос ИИ:")
    return WAITING_QUESTION

# Обработка вопроса к ИИ
async def handle_ai_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    question = update.message.text
    user = update.message.from_user
    
    logger.info(f"User {user.first_name} asked AI: {question}")
    
    await update.message.reply_text("🤔 Думаю...")
    
    ai_response = await ask_ai(question)
    
    await update.message.reply_text(f"💡 ИИ отвечает:\n\n{ai_response}")
    await show_main_menu(update)
    return ConversationHandler.END

# Отмена диалога
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Диалог с ИИ отменен")
    await show_main_menu(update)
    return ConversationHandler.END

# Обработка кнопок меню
async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user = update.message.from_user
    
    logger.info(f"User {user.first_name} pressed: {text}")
    
    responses = {
        "📊 Статус системы": "📊 Система работает стабильно! ✅ Все сервисы доступны.",
        "📋 Помощь": "📋 Задайте мне любой вопрос или нажмите '🤖 Задать вопрос ИИ'",
        "🏠 Главное меню": "menu"
    }
    
    response = responses.get(text)
    
    if response == "menu":
        await show_main_menu(update)
    elif response:
        await update.message.reply_text(response)

# Основная функция
def main():
    try:
        application = Application.builder().token(BOT_TOKEN).build()
        
        # ConversationHandler для диалога с ИИ
        conv_handler = ConversationHandler(
            entry_points=[MessageHandler(filters.Regex("^🤖 Задать вопрос ИИ$"), start_ai_question)],
            states={
                WAITING_QUESTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_ai_question)]
            },
            fallbacks=[CommandHandler("cancel", cancel)]
        )
        
        application.add_handler(CommandHandler("start", start))
        application.add_handler(conv_handler)
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_buttons))
        
        print("🤖 Умный бот с ИИ запущен! (v2)")
        print("🚀 Теперь бот запоминает состояние диалога!")
        
        application.run_polling()
        
    except Exception as e:
        logger.error(f"Ошибка запуска бота: {e}")

if __name__ == '__main__':
    main()
