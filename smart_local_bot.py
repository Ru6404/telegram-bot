from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import logging
import sys
import os
import random
import sqlite3
import datetime

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

# Инициализация базы данных
def init_db():
    conn = sqlite3.connect('bot_history.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            user_name TEXT,
            message_text TEXT,
            bot_response TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Сохранение сообщения в базу данных
def save_message(user_id, user_name, message_text, bot_response):
    try:
        conn = sqlite3.connect('bot_history.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO messages (user_id, user_name, message_text, bot_response)
            VALUES (?, ?, ?, ?)
        ''', (user_id, user_name, message_text, bot_response))
        conn.commit()
        conn.close()
    except Exception as e:
        logger.error(f"Database error: {e}")

# Локальная "нейросеть" - умные ответы
def get_local_ai_response(question):
    question_lower = question.lower()
    
    responses = {
        'новости': [
            "📰 Сегодня в Узбекистане: экономический рост продолжается!",
            "🇺🇿 Важные события: запуск новых социальных программ",
            "🌐 Международные отношения укрепляются",
            "💼 Бизнес-новости: привлечены новые инвестиции"
        ],
        'погода': [
            "🌞 Сегодня отличная погода! +25°C в Ташкенте",
            "☁️ Легкая облачность, +22°C",
            "🌧️ Возможны кратковременные дожди"
        ],
        'курс': [
            "💵 USD: 12500 UZS | EUR: 13500 UZS | RUB: 140 UZS",
            "📊 Курс стабилен: USD ~12400-12600 UZS"
        ],
        'привет': [
            "🤖 Привет! Чем могу помочь?",
            "👋 Здравствуйте! Задайте ваш вопрос",
            "😊 Приветствую! Я готов помочь"
        ],
        'как дела': [
            "✅ Отлично! Работаю без сбоев",
            "🚀 Прекрасно! Готов к вашим вопросам",
            "👍 Хорошо! Чем могу помочь?"
        ],
        'спасибо': [
            "😊 Пожалуйста! Обращайтесь еще!",
            "🌟 Рад был помочь!",
            "🤝 Всегда к вашим услугам!"
        ]
    }
    
    for key in responses:
        if key in question_lower:
            return random.choice(responses[key])
    
    general_responses = [
        "🤔 Интересный вопрос! В Узбекистане много событий",
        "💡 По этой теме лучше обратиться к официальным источникам",
        "📚 Я еще учусь, но скоро смогу отвечать на сложные вопросы",
        "🌟 Сейчас нет свежей информации по этому вопросу",
        "🔍 Попробуйте спросить о новостях, погоде или курсе валют",
        "🇺🇿 Узбекистан активно развивается во всех сферах!",
        "💼 Экономика растет, создаются новые рабочие места",
        "🌍 Страна укрепляет международное сотрудничество"
    ]
    
    return random.choice(general_responses)

# Главное меню
async def show_main_menu(update: Update):
    keyboard = [
        ["📰 Новости", "🌞 Погода"],
        ["💵 Курс валют", "🤖 Задать вопрос"],
        ["📋 Помощь", "🏠 Главное меню"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Выберите действие:", reply_markup=reply_markup)

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    logger.info(f"User {user.first_name} started the bot")
    
    await update.message.reply_text(
        f"🤖 Привет, {user.first_name}!\n"
        "Я умный локальный бот-помощник!\n"
        "Задайте мне вопрос о Узбекистане:"
    )
    await show_main_menu(update)

# Универсальный обработчик текста
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    text = update.message.text
    
    # Обработка состояний
    if context.user_data.get('waiting_question'):
        response = get_local_ai_response(text)
        await update.message.reply_text(f"💡 Ответ:\n\n{response}")
        context.user_data['waiting_question'] = False
        save_message(user.id, user.first_name, text, response)
        return
    
    # Обработка кнопок
    responses = {
        "📰 Новости": lambda: get_local_ai_response("новости"),
        "🌞 Погода": lambda: get_local_ai_response("погода"),
        "💵 Курс валют": lambda: get_local_ai_response("курс"),
        "📋 Помощь": "📋 Задайте вопрос о Узбекистане!",
        "🏠 Главное меню": "menu",
        "🤖 Задать вопрос": "ask_question"
    }
    
    handler = responses.get(text)
    
    if handler == "menu":
        await show_main_menu(update)
        save_message(user.id, user.first_name, text, "menu_shown")
    elif handler == "ask_question":
        await update.message.reply_text("💡 Задайте ваш вопрос:")
        context.user_data['waiting_question'] = True
        save_message(user.id, user.first_name, text, "waiting_question")
    elif handler:
        response = handler() if callable(handler) else handler
        await update.message.reply_text(response)
        save_message(user.id, user.first_name, text, response)
    else:
        response = get_local_ai_response(text)
        await update.message.reply_text(response)
        save_message(user.id, user.first_name, text, response)

# Запуск бота
def main():
    # Инициализируем базу данных
    init_db()
    
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    
    print("🤖 Локальный умный бот запущен!")
    print("🚀 Работает без внешних API - полностью автономно!")
    print("💾 Сохраняет историю в SQLite базе данных")
    print("📊 База данных: bot_history.db")
    
    application.run_polling()

if __name__ == '__main__':
    main()
