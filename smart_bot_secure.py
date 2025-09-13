from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import logging
import sys
import os

# Добавляем путь к текущей папке
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from config import BOT_TOKEN, ADMIN_ID
except ImportError:
    print("❌ Ошибка: Создайте файл config.py с BOT_TOKEN и ADMIN_ID!")
    print("📁 Пример config.py:")
    print("BOT_TOKEN = 'ваш_токен_здесь'")
    print("ADMIN_ID = ваш_айди_здесь")
    sys.exit(1)

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Функция старта
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    logger.info(f"User {user.first_name} started the bot")
    
    await update.message.reply_text(
        f"🤖 Привет, {user.first_name}!\n"
        "Я умный бот для управления системой.\n"
        "Выберите действие из меню ниже:"
    )
    await show_main_menu(update)

# Показать главное меню
async def show_main_menu(update: Update):
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
    
    logger.info(f"User {user.first_name} pressed: {text}")
    
    responses = {
        "👥 Пользователи": "👥 Загружаю список пользователей...",
        "✅ Задачи": "✅ Загружаю список задач...",
        "📊 Статус системы": "📊 Система работает стабильно! ✅ Все сервисы доступны.",
        "📋 Помощь": "📋 Используйте кнопки меню или спросите 'что ты умеешь?'",
        "➕ Создать пользователя": "👤 Для создания пользователя: /add_user Имя Email",
        "➕ Создать задачу": "✅ Для создания задачи: /add_task Заголовок Описание",
        "🛠️ Админ панель": "🛠️ Админ панель: доступно для администраторов",
        "🏠 Главное меню": "menu"
    }
    
    response = responses.get(text, f"Вы сказали: {text}")
    
    if response == "menu":
        await show_main_menu(update)
    else:
        await update.message.reply_text(response)

# Основная функция
def main():
    try:
        application = Application.builder().token(BOT_TOKEN).build()
        
        application.add_handler(CommandHandler("start", start))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_buttons))
        
        print("🤖 Бот запущен! Нажмите Ctrl+C для остановки")
        print(f"🔑 Токен: {BOT_TOKEN[:10]}...")
        print(f"👑 Admin ID: {ADMIN_ID}")
        
        application.run_polling()
        
    except Exception as e:
        logger.error(f"Ошибка запуска бота: {e}")
        print("❌ Проверьте токен и настройки в config.py")

if __name__ == '__main__':
    main()
