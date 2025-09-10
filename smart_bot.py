import os
import logging
import random
import re
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, MessageHandler, filters, ContextTypes, CommandHandler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = "8253068855:AAFPNJke9PYju90RgZe4ZOKOuuMSJNAs0X8"
ADMIN_ID = 123456789  # ← ЗАМЕНИТЕ НА ВАШ ID

def main_menu():
    return ReplyKeyboardMarkup([
        ["👥 Пользователи", "✅ Задачи"],
        ["📊 Статус системы", "📋 Помощь"],
        ["➕ Создать пользователя", "➕ Создать задачу"]
    ], resize_keyboard=True)

def admin_main_menu():
    return ReplyKeyboardMarkup([
        ["👥 Пользователи", "✅ Задачи"],
        ["📊 Статус системы", "📋 Помощь"],
        ["➕ Создать пользователя", "➕ Создать задачу"],
        ["🛠️ Админ панель"]
    ], resize_keyboard=True)

def admin_menu():
    return ReplyKeyboardMarkup([
        ["👥 Все пользователи", "✅ Все задачи"],
        ["📈 Статистика системы", "🔄 Обновить кэш"],
        ["✅ Принять", "❌ Отказ"],
        ["🏠 Главное меню"]
    ], resize_keyboard=True)

# Умные ответы с лучшим пониманием контекста
SMART_RESPONSES = {
    'capabilities': [
        "🤖 Я бот для управления системой! Вот что я умею:\n\n"
        "• 👥 Управление пользователями (список, добавление)\n"
        "• ✅ Работа с задачами (создание, отслеживание)\n"
        "• 📊 Мониторинг статуса системы\n"
        "• 📋 Предоставление помощи и инструкций\n\n"
        "Что именно вас интересует?",
        
        "🎯 Мои основные функции:\n\n"
        "• Работа с пользователями 👥\n"
        "• Управление задачами ✅\n"
        "• Системный мониторинг 📊\n"
        "• Техническая поддержка 📋\n\n"
        "Могу помочь с любым из этих направлений!",
        
        "💡 Я создан для административных задач:\n\n"
        "• 👥 База пользователей\n"
        "• ✅ Система задач\n"
        "• 📊 Статус работы\n"
        "• 🛠️ Администрирование\n\n"
        "Спросите меня о конкретной функции!"
    ],
    'problem_solving': [
        "🔧 К сожалению, я не решаю математические или учебные задачи. "
        "Моя специализация - управление пользователями и задачами в системе. "
        "Но в рамках своих функций я могу помочь отлично!",
        
        "📚 Я не решаю учебные задачи, но могу помочь с:\n"
        "• Организацией рабочих задач ✅\n"
        "• Управлением пользователями 👥\n"
        "• Мониторингом системы 📊\n"
        "Что из этого вас интересует?",
        
        "🎓 Моя цель - помогать с административными задачами, а не с учебными. "
        "Но если у вас есть вопрос по работе системы - я к вашим услугам!"
    ],
    'help_offer': [
        "🆗 Расскажите, чем именно могу помочь? "
        "Мои сильные стороны: пользователи, задачи, системный статус.",
        
        "🤝 Готов помочь! Что вас беспокоит или что нужно сделать?",
        
        "💬 Опишите вашу задачу - посмотрю, чем могу быть полезен!"
    ]
}

def is_admin(user_id):
    return user_id == ADMIN_ID

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    user_id = user.id
    
    await update.message.reply_text(
        f"🚀 Добро пожаловать, {user.first_name}!",
        reply_markup=main_menu() if user_id != ADMIN_ID else admin_main_menu()
    )

async def handle_smart_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    original_text = update.message.text
    user = update.message.from_user
    user_id = user.id
    
    logger.info(f"User {user.first_name}: {original_text}")
    
    # 1. Обработка точных текстов кнопок
    button_handlers = {
        "👥 Пользователи": "👥 Загружаю список пользователей...",
        "✅ Задачи": "✅ Загружаю список задач...",
        "📊 Статус системы": "📊 Система работает стабильно! 🟢 Все сервисы доступны.",
        "📋 Помощь": "📋 Используйте кнопки меню или спросите 'что ты умеешь?'",
        "➕ Создать пользователя": "👤 Для создания пользователя: /add_user Имя Email",
        "➕ Создать задачу": "✅ Для создания задачи: /add_task Заголовок Описание",
        "🛠️ Админ панель": lambda: "🛠️ Админ панель:" if is_admin(user_id) else "❌ Доступ запрещен",
        "🏠 Главное меню": lambda: "🏠 Главное меню:"
    }
    
    if original_text in button_handlers:
        handler = button_handlers[original_text]
        if callable(handler):
            response = handler()
        else:
            response = handler
        
        if original_text == "🏠 Главное меню":
            await update.message.reply_text(response, 
                                          reply_markup=main_menu() if user_id != ADMIN_ID else admin_main_menu())
        elif original_text == "🛠️ Админ панель" and is_admin(user_id):
            await update.message.reply_text(response, reply_markup=admin_menu())
        else:
            await update.message.reply_text(response)
        return
    
    # 2. Интеллектуальный анализ текста
    # Что ты умеешь / возможности
    if any(phrase in text for phrase in ['что ты умеешь', 'твои возможности', 'твой функционал', 
                                       'какие функции', 'что можешь', 'твои способности']):
        await update.message.reply_text(random.choice(SMART_RESPONSES['capabilities']))
        return
    
    # Решение задач
    if any(phrase in text for phrase in ['решить задачу', 'можешь решить', 'реши задачу', 
                                       'помоги с задачей', 'решение задачи']):
        await update.message.reply_text(random.choice(SMART_RESPONSES['problem_solving']))
        return
    
    # Помощь и поддержка
    if any(phrase in text for phrase in ['какую помощь', 'чем помочь', 'можешь помочь', 
                                       'оказать помощь', 'предложи помощь']):
        await update.message.reply_text(random.choice(SMART_RESPONSES['help_offer']))
        return
    
    # Приветствия
    if any(word in text for word in ['привет', 'здравствуй', 'хай', 'добр', 'hello', 'hi']):
        greetings = ["👋 Привет!", "Здравствуйте!", "Приветствую!", "Добро пожаловать!"]
        await update.message.reply_text(f"{random.choice(greetings)} Чем могу помочь?")
        return
    
    # Благодарности
    if any(word in text for word in ['спас', 'благодар', 'thanks', 'thank you']):
        await update.message.reply_text("😊 Всегда рад помочь! Обращайтесь еще!")
        return
    
    # Вопросы (с вопросительными словами)
    if any(word in text for word in ['?', 'как', 'почему', 'что', 'когда', 'где', 'кто', 'зачем']):
        await update.message.reply_text(
            "❓ Хороший вопрос!\n\n"
            "Я специализируюсь на административных задачах:\n"
            "• 👥 Управление пользователями\n"
            "• ✅ Работа с задачами\n"
            "• 📊 Мониторинг системы\n\n"
            "Задайте вопрос в рамках этих тем или используйте кнопки меню!"
        )
        return
    
    # 3. Универсальный ответ для всего остального
    await update.message.reply_text(
        "🤔 Понял ваш запрос!\n\n"
        "Мои основные направления:\n"
        "• 👥 Пользователи и доступы\n"
        "• ✅ Постановка и отслеживание задач\n"
        "• 📊 Состояние системы\n\n"
        "Можете:\n"
        "• Использовать кнопки меню 📋\n"
        "• Спросить 'что ты умеешь?' 🤖\n"
        "• Написать 'помощь' для инструкций 🆘"
    )

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_smart_message))
    
    logger.info("🤖 Умный бот запущен...")
    print("✅ Бот запущен! Теперь он понимает естественный язык!")
    print("🎯 Протестируйте: 'что ты умеешь', 'можешь решить задачу', 'какую помощь оказать'")
    
    application.run_polling()

if __name__ == "__main__":
    main()
