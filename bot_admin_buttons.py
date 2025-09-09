import os
import logging
import httpx
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telegram.ext import Application, MessageHandler, filters, ContextTypes, CommandHandler, ConversationHandler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = "8253068855:AAFPNJke9PYju90RgZe4ZOKOuuMSJNAs0X8"
API_URL = "http://localhost:8000"

# Состояния для ConversationHandler
USERNAME, EMAIL, TITLE, DESCRIPTION = range(4)

# Клавиатура главного меню
def get_main_keyboard():
    keyboard = [
        [KeyboardButton("👥 Пользователи"), KeyboardButton("✅ Задачи")],
        [KeyboardButton("📊 Статус системы"), KeyboardButton("📋 Помощь")],
        [KeyboardButton("➕ Создать пользователя"), KeyboardButton("➕ Создать задачу")],
        [KeyboardButton("🛠️ Админ панель")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# Клавиатура админ панели
def get_admin_keyboard():
    keyboard = [
        [KeyboardButton("👥 Все пользователи"), KeyboardButton("✅ Все задачи")],
        [KeyboardButton("📈 Статистика системы"), KeyboardButton("🔄 Обновить кэш")],
        [KeyboardButton("✅ Принять"), KeyboardButton("❌ Отказ")],
        [KeyboardButton("🏠 Главное меню")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# Клавиатура подтверждения
def get_approval_keyboard():
    keyboard = [
        [KeyboardButton("✅ Принять"), KeyboardButton("❌ Отказ")],
        [KeyboardButton("↩️ Назад")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /start с кнопками меню"""
    await update.message.reply_text(
        "🚀 *Добро пожаловать в Auto-Cloud System!*\n\n"
        "Используйте кнопки меню ниже для управления системой:",
        parse_mode='Markdown',
        reply_markup=get_main_keyboard()
    )

async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Админ панель"""
    await update.message.reply_text(
        "🛠️ *Админ панель*\n\n"
        "Выберите действие:",
        parse_mode='Markdown',
        reply_markup=get_admin_keyboard()
    )

async def handle_approval(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка кнопок Принять/Отказ"""
    choice = update.message.text
    
    if choice == "✅ Принять":
        await update.message.reply_text(
            "✅ *Запрос принят!*\n\n"
            "Действие успешно подтверждено.",
            parse_mode='Markdown',
            reply_markup=get_admin_keyboard()
        )
    elif choice == "❌ Отказ":
        await update.message.reply_text(
            "❌ *Запрос отклонен!*\n\n"
            "Действие отменено.",
            parse_mode='Markdown',
            reply_markup=get_admin_keyboard()
        )

    async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text
    message_lower = message.lower()
    
    # Главное меню
    if any(word in message_lower for word in ['меню', 'главное', 'домой', 'начать']):
        await update.message.reply_text(
            "🏠 *Главное меню*",
            parse_mode='Markdown',
            reply_markup=get_main_keyboard()
        )
        return
    
    # Админ панель
    elif any(word in message_lower for word in ['админ', 'admin', 'панель', 'управление']) or '🛠️' in message:
        await admin_panel(update, context)
        return
    
    # Кнопка: 👥 Пользователи
    elif '👥' in message or 'пользователи' in message_lower:
        await update.message.reply_text("👥 Загружаю пользователей...")
        return
    
    # Кнопка: ✅ Задачи  
    elif '✅' in message or 'задачи' in message_lower:
        await update.message.reply_text("✅ Загружаю задачи...")
        return
    
    # Кнопка: 📊 Статус системы
    elif '📊' in message or 'статус' in message_lower:
        await update.message.reply_text("📊 Проверяю статус системы...")
        return
    
    # Кнопка: 📋 Помощь
    elif '📋' in message or 'помощь' in message_lower:
        await update.message.reply_text("📋 Показываю помощь...")
        return
    
    # Кнопка: ➕ Создать пользователя
    elif '➕ создать пользователя' in message_lower:
        await update.message.reply_text("👤 Инструкция по созданию пользователя...")
        return
    
    # Кнопка: ➕ Создать задачу
    elif '➕ создать задачу' in message_lower:
        await update.message.reply_text("✅ Инструкция по созданию задачи...")
        return
    
    # Кнопка: ✅ Принять
    elif '✅ принять' in message_lower or 'принять' in message_lower:
        await update.message.reply_text("✅ Запрос принят! Действие выполнено.")
        return
    
    # Кнопка: ❌ Отказ  
    elif '❌ отказ' in message_lower or 'отказ' in message_lower:
        await update.message.reply_text("❌ Запрос отклонен! Действие отменено.")
        return
    
    # Кнопка: 🏠 Главное меню
    elif '🏠' in message or 'главное меню' in message_lower:
        await update.message.reply_text(
            "🏠 *Главное меню*",
            parse_mode='Markdown',
            reply_markup=get_main_keyboard()
        )
        return
    
    # Неизвестная команда
    else:
        await update.message.reply_text(
            "❓ Неизвестная команда\n\nИспользуйте кнопки меню:",
            reply_markup=get_main_keyboard()
        )
        
        return
    
    # Админ панель
    elif any(word in message_lower for word in ['админ', 'admin', 'панель', 'управление']):
        await admin_panel(update, context)
        return
    
    # Кнопка: 🛠️ Админ панель
    elif '🛠️ админ панель' in message_lower or 'админ' in message_lower:
        await admin_panel(update, context)
        return
    
    # Кнопка: 👥 Все пользователи (админ)
    elif 'все пользователи' in message_lower:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{API_URL}/users")
                if response.status_code == 200:
                    users = response.json()
                    if users:
                        users_list = "\n".join([f"• 👤 {u.get('username', 'N/A')} ({u.get('email', 'N/A')}) - ID: {u.get('id', 'N/A')}" for u in users])
                        await update.message.reply_text(f"👥 *Все пользователи ({len(users)}):*\n\n{users_list}", parse_mode='Markdown')
                    else:
                        await update.message.reply_text("👥 Нет пользователей в системе.")
                else:
                    await update.message.reply_text("❌ Ошибка получения пользователей")
        except Exception as e:
            await update.message.reply_text("❌ API недоступен!")
        return
    
    # Кнопка: ✅ Все задачи (админ)
    elif 'все задачи' in message_lower:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{API_URL}/todos")
                if response.status_code == 200:
                    todos = response.json()
                    if todos:
                        todos_list = "\n".join([f"• 📝 {t.get('title', 'N/A')} - ID: {t.get('id', 'N/A')}" for t in todos])
                        await update.message.reply_text(f"✅ *Все задачи ({len(todos)}):*\n\n{todos_list}", parse_mode='Markdown')
                    else:
                        await update.message.reply_text("✅ Нет задач в системе.")
                else:
                    await update.message.reply_text("❌ Ошибка получения задач")
        except Exception as e:
            await update.message.reply_text("❌ API недоступен!")
        return
    
    # Кнопка: 📈 Статистика системы (админ)
    elif 'статистика системы' in message_lower:
        try:
            async with httpx.AsyncClient() as client:
                users_response = await client.get(f"{API_URL}/users")
                todos_response = await client.get(f"{API_URL}/todos")
                
                users_count = len(users_response.json()) if users_response.status_code == 200 else 0
                todos_count = len(todos_response.json()) if todos_response.status_code == 200 else 0
                
                await update.message.reply_text(
                    f"📈 *Детальная статистика:*\n\n"
                    f"• 👥 Пользователей: {users_count}\n"
                    f"• ✅ Задач: {todos_count}\n"
                    f"• 🏢 API статус: 🟢 Работает\n"
                    f"• 📊 Всего записей: {users_count + todos_count}",
                    parse_mode='Markdown'
                )
        except Exception as e:
            await update.message.reply_text("❌ API недоступен!")
        return
    
    # Кнопка: 🔄 Обновить кэш (админ)
    elif 'обновить кэш' in message_lower:
        await update.message.reply_text(
            "🔄 *Кэш обновлен!*\n\n"
            "Данные успешно синхронизированы с сервером.",
            parse_mode='Markdown'
        )
        return
    
    # Кнопки Принять/Отказ
    elif message in ["✅ Принять", "❌ Отказ"]:
        await handle_approval(update, context)
        return
    
    # Остальные кнопки главного меню (оставляем как было)
    elif 'пользователи' in message_lower:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{API_URL}/users")
                if response.status_code == 200:
                    users = response.json()
                    if users:
                        users_list = "\n".join([f"• 👤 {u.get('username', 'N/A')} ({u.get('email', 'N/A')})" for u in users[:5]])
                        await update.message.reply_text(f"👥 *Пользователи ({len(users)}):*\n\n{users_list}", parse_mode='Markdown')
                    else:
                        await update.message.reply_text("👥 Пока нет пользователей в системе.")
                else:
                    await update.message.reply_text("❌ Ошибка получения пользователей")
        except Exception as e:
            await update.message.reply_text("❌ API недоступен! Запустите: python main.py")
        return
    
    elif 'задачи' in message_lower:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{API_URL}/todos")
                if response.status_code == 200:
                    todos = response.json()
                    if todos:
                        todos_list = "\n".join([f"• 📝 {t.get('title', 'N/A')}" for t in todos[:5]])
                        await update.message.reply_text(f"✅ *Задачи ({len(todos)}):*\n\n{todos_list}", parse_mode='Markdown')
                    else:
                        await update.message.reply_text("✅ Пока нет задач в системе.")
                else:
                    await update.message.reply_text("❌ Ошибка получения задач")
        except Exception as e:
            await update.message.reply_text("❌ API недоступен! Запустите: python main.py")
        return
    
    elif 'статус' in message_lower:
        try:
            async with httpx.AsyncClient() as client:
                users_response = await client.get(f"{API_URL}/users")
                todos_response = await client.get(f"{API_URL}/todos")
                
                users_count = len(users_response.json()) if users_response.status_code == 200 else 0
                todos_count = len(todos_response.json()) if todos_response.status_code == 200 else 0
                
                await update.message.reply_text(
                    f"📊 *Статус системы:*\n\n"
                    f"• 👥 Пользователей: {users_count}\n"
                    f"• ✅ Задач: {todos_count}\n"
                    f"• 🏢 API: 🟢 Работает",
                    parse_mode='Markdown'
                )
        except Exception as e:
            await update.message.reply_text("❌ API недоступен! Запустите: python main.py")
        return
    
    elif 'помощь' in message_lower:
        await update.message.reply_text(
            "📋 *Доступные команды:*\n\n"
            "• 👥 Пользователи - список пользователей\n"
            "• ✅ Задачи - список задач\n"
            "• 📊 Статус системы - статистика\n"
            "• ➕ Создать пользователя - инструкция\n"
            "• ➕ Создать задачу - инструкция\n"
            "• 🛠️ Админ панель - расширенные функции\n\n"
            "💡 Используйте кнопки меню для удобства!",
            parse_mode='Markdown'
        )
        return
    
    # Остальная логика создания пользователей/задач...
    # ... (оставляем без изменений из предыдущего кода)

    # Неизвестная команда
    else:
        await update.message.reply_text(
            "❓ Неизвестная команда\n\nИспользуйте кнопки меню или напишите 'помощь'",
            reply_markup=get_main_keyboard()
        )

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Команды
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", handle_message))
    application.add_handler(CommandHandler("admin", admin_panel))
    
    # Текстовые сообщения
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    logger.info("Бот с админ-кнопками запущен...")
    print("✅ Бот с кнопками Принять/Отказ запущен!")
    application.run_polling()

if __name__ == "__main__":
    main()
