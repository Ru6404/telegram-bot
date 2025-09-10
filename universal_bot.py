import os
import logging
import random
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, MessageHandler, filters, ContextTypes, CommandHandler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = "8253068855:AAFPNJke9PYju90RgZe4ZOKOuuMSJNAs0X8"

# ЗАМЕНИТЕ ЭТОТ ID НА ВАШ РЕАЛЬНЫЙ TELEGRAM ID
ADMIN_ID = 123456789  # ← ВАШ ID ЗДЕСЬ

# Главное меню (для всех пользователей)
def main_menu():
    return ReplyKeyboardMarkup([
        ["👥 Пользователи", "✅ Задачи"],
        ["📊 Статус системы", "📋 Помощь"],
        ["➕ Создать пользователя", "➕ Создать задачу"]
    ], resize_keyboard=True)

# Админ меню (только для админа)
def admin_menu():
    return ReplyKeyboardMarkup([
        ["👥 Все пользователи", "✅ Все задачи"],
        ["📈 Статистика системы", "🔄 Обновить кэш"],
        ["✅ Принять", "❌ Отказ"],
        ["🏠 Главное меню"]
    ], resize_keyboard=True)

# Меню для админа (включает админскую панель)
def admin_main_menu():
    return ReplyKeyboardMarkup([
        ["👥 Пользователи", "✅ Задачи"],
        ["📊 Статус системы", "📋 Помощь"],
        ["➕ Создать пользователя", "➕ Создать задачу"],
        ["🛠️ Админ панель"]
    ], resize_keyboard=True)

# Ответы на разные типы сообщений
RESPONSES = {
    'greeting': [
        "👋 Привет! Как дела?",
        "Приветствую! Чем могу помочь?",
        "Здравствуйте! Рад вас видеть!",
        "Привет! Готов помочь с задачами!",
        "👋 Добро пожаловать! Что вас интересует?"
    ],
    'thanks': [
        "😊 Всегда рад помочь!",
        "Пожалуйста! Обращайтесь еще!",
        "Рад был помочь!",
        "Не за что! Если что - я тут!",
        "Спасибо вам за обращение!"
    ],
    'farewell': [
        "👋 До свидания! Хорошего дня!",
        "Пока! Возвращайтесь скорее!",
        "До встречи! Буду ждать ваших вопросов!",
        "Всего доброго! Не пропадайте!",
        "Пока! Если что - я на связи!"
    ],
    'unknown': [
        "🤔 Интересный вопрос! Попробуйте использовать кнопки меню",
        "Пока не могу ответить на это. Используйте команды из меню!",
        "Не совсем понимаю. Может, спросите по-другому?",
        "Это вне моей компетенции. Попробуйте 'Помощь'",
        "Хм... Лучше использовать стандартные команды"
    ],
    'help': [
        "📋 Вот что я умею: управление пользователями и задачами!",
        "Помощь уже здесь! Используйте кнопки меню для навигации",
        "Я помогу! Выберите нужный раздел в меню",
        "Готов помочь! Что вас интересует: пользователи или задачи?",
        "Спрашивайте! Мои функции: 👥 пользователи, ✅ задачи, 📊 статус"
    ]
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    user_id = user.id
    
    await update.message.reply_text(
        f"🚀 Добро пожаловать, {user.first_name}!",
        reply_markup=main_menu() if user_id != ADMIN_ID else admin_main_menu()
    )

def is_admin(user_id):
    return user_id == ADMIN_ID

async def handle_any_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    user = update.message.from_user
    user_id = user.id
    
    logger.info(f"User {user.first_name} said: {update.message.text}")
    
    # Определяем тип сообщения
    message_type = 'unknown'
    
    # Приветствия
    if any(word in text for word in ['привет', 'hello', 'hi', 'здравствуй', 'хай', 'добрый', 'начать']):
        message_type = 'greeting'
    
    # Благодарности
    elif any(word in text for word in ['спасибо', 'благодарю', 'thanks', 'thank you', 'мерси']):
        message_type = 'thanks'
    
    # Прощания
    elif any(word in text for word in ['пока', 'до свидания', 'bye', 'goodbye', 'всего', 'увидимся']):
        message_type = 'farewell'
    
    # Помощь
    elif any(word in text for word in ['помощь', 'help', 'справка', 'команды', 'что ты умеешь', 'функции']):
        message_type = 'help'
    
    # Вопросы
    elif any(word in text for word in ['как', 'почему', 'что', 'когда', 'где', 'кто', 'зачем']):
        message_type = 'question'
    
    # Обработка кнопок (точные совпадения)
    original_text = update.message.text
    
    if original_text == "👥 Пользователи":
        await update.message.reply_text("👥 Загружаю список пользователей...")
        return
    
    elif original_text == "✅ Задачи":
        await update.message.reply_text("✅ Загружаю список задач...")
        return
    
    elif original_text == "📊 Статус системы":
        await update.message.reply_text("📊 Система работает стабильно! 🟢")
        return
    
    elif original_text == "📋 Помощь":
        await update.message.reply_text("📋 Используйте кнопки меню для навигации")
        return
    
    elif original_text == "➕ Создать пользователя":
        await update.message.reply_text("👤 Для создания: /add_user Имя Email")
        return
    
    elif original_text == "➕ Создать задачу":
        await update.message.reply_text("✅ Для создания: /add_task Заголовок Описание")
        return
    
    # Админские функции
    elif original_text == "🛠️ Админ панель" and is_admin(user_id):
        await update.message.reply_text("🛠️ Админ панель:", reply_markup=admin_menu())
        return
    
    elif original_text in ["✅ Принять", "❌ Отказ", "👥 Все пользователи", 
                          "✅ Все задачи", "📈 Статистика системы", "🔄 Обновить кэш"] and is_admin(user_id):
        # Обработка админских кнопок
        pass
    
    elif original_text == "🏠 Главное меню":
        await update.message.reply_text("🏠 Главное меню:", 
                                      reply_markup=main_menu() if user_id != ADMIN_ID else admin_main_menu())
        return
    
    # Отправляем ответ в зависимости от типа сообщения
    if message_type == 'greeting':
        response = random.choice(RESPONSES['greeting'])
        await update.message.reply_text(response)
    
    elif message_type == 'thanks':
        response = random.choice(RESPONSES['thanks'])
        await update.message.reply_text(response)
    
    elif message_type == 'farewell':
        response = random.choice(RESPONSES['farewell'])
        await update.message.reply_text(response)
    
    elif message_type == 'help':
        response = random.choice(RESPONSES['help'])
        await update.message.reply_text(response + "\n\nДоступные разделы:\n• 👥 Пользователи\n• ✅ Задачи\n• 📊 Статус\n• 📋 Помощь")
    
    elif message_type == 'question':
        await update.message.reply_text(
            "❓ Хороший вопрос!\n\n"
            "Я специализируюсь на:\n"
            "• Управлении пользователями 👥\n"
            "• Работе с задачами ✅\n"
            "• Мониторинге системы 📊\n\n"
            "Задайте вопрос в рамках этих тем или используйте кнопки меню!"
        )
    
    else:
        # Для любых других сообщений
        response = random.choice(RESPONSES['unknown'])
        await update.message.reply_text(
            f"{response}\n\n"
            "Попробуйте:\n"
            "• Написать 'привет' 👋\n"
            "• Спросить 'что ты умеешь?' 🤔\n"
            "• Использовать кнопки меню 📋\n"
            "• Написать 'помощь' для списка команд"
        )

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_any_message))
    
    logger.info("🤖 Универсальный бот запущен...")
    print("✅ Бот запущен! Теперь он отвечает на ЛЮБЫЕ сообщения!")
    print("🎯 Протестируйте: напишите 'привет', 'как дела?', 'что ты умеешь?'")
    
    application.run_polling()

if __name__ == "__main__":
    main()
