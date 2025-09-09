import os
import logging
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
        # Кнопка "Админ панель" убрана для обычных пользователей
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
        ["🛠️ Админ панель"]  # Только админ видит эту кнопку
    ], resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    user_id = user.id
    
    # Показываем ID пользователю (чтобы вы могли узнать свой ID)
    await update.message.reply_text(
        f"🚀 Добро пожаловать, {user.first_name}! Ваш ID: {user_id}",
        reply_markup=main_menu() if user_id != ADMIN_ID else admin_main_menu()
    )

# Проверка является ли пользователь админом
def is_admin(user_id):
    return user_id == ADMIN_ID

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user = update.message.from_user
    user_id = user.id
    
    logger.info(f"User {user.first_name} (ID: {user_id}) pressed: {text}")
    
    # Обработка кнопок для всех пользователей
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
    
    # Админские кнопки (только для админа)
    elif text == "🛠️ Админ панель":
        if is_admin(user_id):
            await update.message.reply_text(
                "🛠️ Добро пожаловать в админ панель!",
                reply_markup=admin_menu()
            )
        else:
            await update.message.reply_text("❌ Неизвестная команда.")
    
    elif text in ["✅ Принять", "❌ Отказ", "👥 Все пользователи", 
                 "✅ Все задачи", "📈 Статистика системы", "🔄 Обновить кэш"]:
        if is_admin(user_id):
            if text == "✅ Принять":
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
        else:
            await update.message.reply_text("❌ Неизвестная команда.")
    
    elif text == "🏠 Главное меню":
        await update.message.reply_text(
            "🏠 Главное меню:",
            reply_markup=main_menu() if user_id != ADMIN_ID else admin_main_menu()
        )
    
    # Текстовые команды
    elif "привет" in text.lower():
        await update.message.reply_text("👋 Привет! Используйте кнопки меню:")
    
    elif "помощь" in text.lower():
        await update.message.reply_text("📋 Выберите нужный раздел через кнопки меню")
    
    else:
        await update.message.reply_text(
            "❓ Не понимаю команду. Используйте кнопки меню:",
            reply_markup=main_menu() if user_id != ADMIN_ID else admin_main_menu()
        )

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    logger.info("🤖 Бот запущен с эксклюзивной админской панелью...")
    print("✅ Бот запущен! Админская панель доступна только вам!")
    print(f"⚠️  Не забудьте заменить ADMIN_ID на ваш реальный ID!")
    
    application.run_polling()

if __name__ == "__main__":
    main()
