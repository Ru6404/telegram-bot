import os
import logging
import httpx
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, MessageHandler, filters, ContextTypes, CommandHandler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = "8253068855:AAFPNJke9PYju90RgZe4ZOKOuuMSJNAs0X8"
API_URL = "http://localhost:8000"

# Клавиатура меню
def get_main_keyboard():
    keyboard = [
        [KeyboardButton("👥 Пользователи"), KeyboardButton("✅ Задачи")],
        [KeyboardButton("📊 Статус системы"), KeyboardButton("📋 Помощь")],
        [KeyboardButton("➕ Создать пользователя"), KeyboardButton("➕ Создать задачу")]
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

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text
    message_lower = message.lower()
    
    # Приветствия
    if any(word in message_lower for word in ['привет', 'hello', 'hi', 'start', 'начать']):
        await update.message.reply_text(
            "👋 Привет! Используйте кнопки меню для управления Auto-Cloud системой!",
            reply_markup=get_main_keyboard()
        )
        return
    
    # Кнопка: 👥 Пользователи
    elif 'пользователи' in message_lower:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{API_URL}/users")
                if response.status_code == 200:
                    users = response.json()
                    if users:
                        users_list = "\n".join([f"• 👤 {u.get('username', 'N/A')} ({u.get('email', 'N/A')})" for u in users[:10]])
                        await update.message.reply_text(f"👥 *Пользователи ({len(users)}):*\n\n{users_list}", parse_mode='Markdown')
                    else:
                        await update.message.reply_text("👥 Пока нет пользователей в системе.")
                else:
                    await update.message.reply_text("❌ Ошибка получения пользователей")
        except Exception as e:
            await update.message.reply_text("❌ API недоступен! Запустите: python main.py")
        return
    
    # Кнопка: ✅ Задачи
    elif 'задачи' in message_lower:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{API_URL}/todos")
                if response.status_code == 200:
                    todos = response.json()
                    if todos:
                        todos_list = "\n".join([f"• 📝 {t.get('title', 'N/A')}" for t in todos[:10]])
                        await update.message.reply_text(f"✅ *Задачи ({len(todos)}):*\n\n{todos_list}", parse_mode='Markdown')
                    else:
                        await update.message.reply_text("✅ Пока нет задач в системе.")
                else:
                    await update.message.reply_text("❌ Ошибка получения задач")
        except Exception as e:
            await update.message.reply_text("❌ API недоступен! Запустите: python main.py")
        return
    
    # Кнопка: 📊 Статус системы
    elif 'статус' in message_lower or 'статистика' in message_lower:
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
    
    # Кнопка: 📋 Помощь
    elif 'помощь' in message_lower or 'команды' in message_lower:
        await update.message.reply_text(
            "📋 *Доступные команды:*\n\n"
            "• 👥 Пользователи - список пользователей\n"
            "• ✅ Задачи - список задач\n"
            "• 📊 Статус системы - статистика\n"
            "• ➕ Создать пользователя - инструкция\n"
            "• ➕ Создать задачу - инструкция\n\n"
            "💡 Также можно писать текстовые команды:",
            parse_mode='Markdown'
        )
        return
    
    # Кнопка: ➕ Создать пользователя
    elif 'создать пользователя' in message_lower and not message_lower.startswith('как'):
        await update.message.reply_text(
            "👤 *Создание пользователя:*\n\n"
            "Используйте формат:\n"
            "`добавить пользователя: Иван, ivan@mail.ru`\n\n"
            "Пример:\n"
            "`добавить пользователя: Алексей, alex@company.com`",
            parse_mode='Markdown'
        )
        return
    
    # Кнопка: ➕ Создать задачу
    elif 'создать задачу' in message_lower and not message_lower.startswith('как'):
        await update.message.reply_text(
            "✅ *Создание задачи:*\n\n"
            "Используйте формат:\n"
            "`добавить задачу: Заголовок, Описание`\n\n"
            "Пример:\n"
            "`добавить задачу: Разработка API, Создать REST API для системы`",
            parse_mode='Markdown'
        )
        return
    
    # Создание пользователя (текстовый ввод)
    elif 'добавить пользователя:' in message_lower:
        try:
            parts = message.split(':', 1)[1].strip().split(',')
            if len(parts) >= 2:
                username = parts[0].strip()
                email = parts[1].strip()
                
                async with httpx.AsyncClient() as client:
                    response = await client.post(f"{API_URL}/users", json={
                        "username": username,
                        "email": email
                    })
                    
                    if response.status_code == 200:
                        user = response.json()
                        await update.message.reply_text(
                            f"✅ *Пользователь создан!*\n\n"
                            f"👤 Имя: {user.get('username', 'N/A')}\n"
                            f"📧 Email: {user.get('email', 'N/A')}\n"
                            f"🆔 ID: {user.get('id', 'N/A')}",
                            parse_mode='Markdown'
                        )
                    else:
                        await update.message.reply_text("❌ Ошибка создания пользователя")
        except:
            await update.message.reply_text("❌ Неверный формат. Используйте: `добавить пользователя: Иван, ivan@mail.ru`")
        return
    
    # Создание задачи (текстовый ввод)
    elif 'добавить задачу:' in message_lower:
        try:
            parts = message.split(':', 1)[1].strip().split(',')
            if len(parts) >= 2:
                title = parts[0].strip()
                description = parts[1].strip()
                
                async with httpx.AsyncClient() as client:
                    response = await client.post(f"{API_URL}/todos", json={
                        "title": title,
                        "description": description
                    })
                    
                    if response.status_code == 200:
                        todo = response.json()
                        await update.message.reply_text(
                            f"✅ *Задача создана!*\n\n"
                            f"📝 Заголовок: {todo.get('title', 'N/A')}\n"
                            f"📋 Описание: {todo.get('description', 'N/A')}\n"
                            f"🆔 ID: {todo.get('id', 'N/A')}",
                            parse_mode='Markdown'
                        )
                    else:
                        await update.message.reply_text("❌ Ошибка создания задачи")
        except:
            await update.message.reply_text("❌ Неверный формат. Используйте: `добавить задачу: Заголовок, Описание`")
        return
    
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
    
    # Текстовые сообщения
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    logger.info("Бот с меню запущен...")
    print("✅ Бот с кнопками меню запущен!")
    application.run_polling()

if __name__ == "__main__":
    main()
