from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import os
import logging

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Токен бота
BOT_TOKEN = os.getenv('BOT_TOKEN', '8253068855:AAFPNJke9PYju90RgZe4ZOKOuuMSJNAs0X8')

# Функция старта
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    logger.info(f"User {user.first_name} started the bot")
    
    # Приветственное сообщение
    await update.message.reply_text(
        f"🤖 Привет, {user.first_name}!\n"
        "Я умный бот для управления системой.\n"
        "Выберите действие из меню ниже:"
    )
    
    # Создаем кнопки меню
    keyboard = [
        ["👥 Пользователи", "✅ Задачи"],
        ["📊 Статус системы", "📋 Помощь"],
        ["➕ Создать пользователя", "➕ Создать задачу"],
        ["🛠️ Админ панель", "🏠 Главное меню"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Выберите действие:", reply_markup=reply_markup)

# Обработка кнопок меню
async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user = update.message.from_user
    
    logger.info(f"User {user.first_name} pressed button: {text}")
    
    # Обработка конкретных кнопок
    if text == "👥 Пользователи":
        await update.message.reply_text("👥 Загружаю список пользователей...")
    elif text == "✅ Задачи":
        await update.message.reply_text("✅ Загружаю список задач...")
    elif text == "📊 Статус системы":
        await update.message.reply_text("📊 Система работает стабильно! ✅ Все сервисы доступны.")
    elif text == "📋 Помощь":
        await update.message.reply_text("📋 Используйте кнопки меню или спросите 'что ты умеешь?'")
    elif text == "➕ Создать пользователя":
        await update.message.reply_text("👤 Для создания пользователя: /add_user Имя Email")
    elif text == "➕ Создать задача":
        await update.message.reply_text("✅ Для создания задачи: /add_task Заголовок Описание")
    elif text == "🛠️ Админ панель":
        await update.message.reply_text("🛠️ Админ панель: доступно для администраторов")
    elif text == "🏠 Главное меню":
        # Обновляем меню
        keyboard = [
            ["👥 Пользователи", "✅ Задачи"],
            ["📊 Статус системы", "📋 Помощь"],
            ["➕ Создать пользователя", "➕ Создать задача"],
            ["🛠️ Админ панель", "🏠 Главное меню"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text("🏠 Главное меню:", reply_markup=reply_markup)
    else:
        await update.message.reply_text(f"Вы сказали: {text}")

# Основная функция
def main():
    # Создаем приложение
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Добавляем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_buttons))
    
    # Запускаем бота
    print("🤖 Бот запущен! Нажмите Ctrl+C для остановки")
    application.run_polling()

if __name__ == '__main__':
    main()
