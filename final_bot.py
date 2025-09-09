import os
import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, MessageHandler, filters, ContextTypes, CommandHandler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = "8253068855:AAFPNJke9PYju90RgZe4ZOKOuuMSJNAs0X8"

# Главное меню
def main_menu():
    return ReplyKeyboardMarkup([
        ["👥 Пользователи", "✅ Задачи"],
        ["📊 Статус системы", "📋 Помощь"],
        ["➕ Создать пользователя", "➕ Создать задачу"],
        ["🛠️ Админ панель"]
    ], resize_keyboard=True)

# Админ меню
def admin_menu():
    return ReplyKeyboardMarkup([
        ["👥 Все пользователи", "✅ Все задачи"],
        ["📈 Статистика системы", "🔄 Обновить кэш"],
        ["✅ Принять", "❌ Отказ"],
        ["🏠 Главное меню"]
    ], resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 Добро пожаловать! Выберите действие:",
        reply_markup=main_menu()
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user = update.message.from_user
    
    logger.info(f"User {user.first_name} pressed: {text}")
    
    # Обработка всех кнопок
    if text == "👥 Пользователи":
        await update.message.reply_text("👥 Список пользователей загружается...")
    
    elif text == "✅ Задачи":
        await update.message.reply_text("✅ Список задач загружается...")
    
    elif text == "📊 Статус системы":
        await update.message.reply_text("📊 Статус системы: 🟢 Все работает!")
    
    elif text == "📋 Помощь":
        await update.message.reply_text("📋 Помощь: Используйте кнопки меню для навигации")
    
    elif text == "➕ Создать пользователя":
        await update.message.reply_text("👤 Для создания пользователя используйте: добавить пользователя: Имя, email@example.com")
    
    elif text == "➕ Создать задачу":
        await update.message.reply_text("✅ Для создания задачи используйте: добавить задачу: Заголовок, Описание")
    
    elif text == "🛠️ Админ панель":
        await update.message.reply_text(
            "🛠️ Админ панель:",
            reply_markup=admin_menu()
        )
    
    # Админские кнопки
    elif text == "✅ Принять":
        await update.message.reply_text("✅ Запрос принят! Действие выполнено.")
    
    elif text == "❌ Отказ":
        await update.message.reply_text("❌ Запрос отклонен! Действие отменено.")
    
    elif text == "👥 Все пользователи":
        await update.message.reply_text("👥 Полный список пользователей...")
    
    elif text == "✅ Все задачи":
        await update.message.reply_text("✅ Полный список задач...")
    
    elif text == "📈 Статистика системы":
        await update.message.reply_text("📈 Статистика: Пользователей: 0, Задач: 0")
    
    elif text == "🔄 Обновить кэш":
        await update.message.reply_text("🔄 Кэш обновлен!")
    
    elif text == "🏠 Главное меню":
        await update.message.reply_text(
            "🏠 Главное меню:",
            reply_markup=main_menu()
        )
    
    # Текстовые команды
    elif "привет" in text.lower():
        await update.message.reply_text("👋 Привет! Используйте кнопки меню:")
    
    elif "помощь" in text.lower():
        await update.message.reply_text("📋 Выберите нужный раздел через кнопки меню")
    
    else:
        await update.message.reply_text(
            "❓ Не понимаю команду. Используйте кнопки меню:",
            reply_markup=main_menu()
        )

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    logger.info("🤖 Бот запущен с кнопками меню...")
    print("✅ Бот запущен! Все кнопки будут работать!")
    
    application.run_polling()

if __name__ == "__main__":
    main()
