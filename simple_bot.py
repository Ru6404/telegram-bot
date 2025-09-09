import os
import logging
from datetime import datetime
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes, CommandHandler

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = "8253068855:AAFPNJke9PYju90RgZe4ZOKOuuMSJNAs0X8"

# Базы данных в памяти (как в Auto-Cloud API)
users_db = []
todos_db = []

async def process_message(message: str, user_id: int) -> str:
    message_lower = message.lower().strip()
    
    # Статистика
    if 'статистика' in message_lower:
        return f"📊 *Статистика:*\n👥 Пользователей: {len(users_db)}\n✅ Задач: {len(todos_db)}"
    
    # Пользователи
    elif 'пользователи' in message_lower:
        if not users_db:
            return "👥 Нет пользователей"
        users_list = "\n".join([f"• {u['username']} ({u['email']})" for u in users_db])
        return f"👥 Пользователи:\n{users_list}"
    
    # Задачи
    elif 'задачи' in message_lower:
        if not todos_db:
            return "✅ Нет задач"
        todos_list = "\n".join([f"• {t['title']}" for t in todos_db])
        return f"✅ Задачи:\n{todos_list}"
    
    # Создать пользователя
    elif 'создать пользователя' in message_lower:
        try:
            parts = message.split(' ', 2)
            if len(parts) >= 3:
                username = parts[2].split(' ')[0]
                email = parts[2].split(' ')[1] if len(parts[2].split(' ')) > 1 else f"{username}@mail.ru"
                
                user = {
                    "id": len(users_db) + 1,
                    "username": username,
                    "email": email,
                    "created_at": datetime.now().isoformat()
                }
                users_db.append(user)
                return f"✅ Пользователь создан!\n👤 {username}\n📧 {email}"
        except:
            return "❌ Используйте: 'создать пользователя Иван email@mail.ru'"
    
    # Создать задачу
    elif 'создать задачу' in message_lower:
        try:
            parts = message.split(' ', 2)
            if len(parts) >= 3:
                title = parts[2].split(' ', 1)[0]
                description = parts[2].split(' ', 1)[1] if len(parts[2].split(' ', 1)) > 1 else "Описание"
                
                todo = {
                    "id": len(todos_db) + 1,
                    "title": title,
                    "description": description,
                    "created_at": datetime.now().isoformat()
                }
                todos_db.append(todo)
                return f"✅ Задача создана!\n📝 {title}\n📋 {description}"
        except:
            return "❌ Используйте: 'создать задачу Заголовок Описание'"
    
    # Помощь
    elif 'помощь' in message_lower:
        return "🚀 Команды:\n• статистика\n• пользователи\n• задачи\n• создать пользователя Иван mail@mail.ru\n• создать задачу Заголовок Описание"
    
    else:
        return "❓ Напишите 'помощь' для списка команд"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        response = await process_message(update.message.text, update.message.from_user.id)
        await update.message.reply_text(response, parse_mode='Markdown')
    except Exception as e:
        logger.error(f"Ошибка: {e}")
        await update.message.reply_text("⚠️ Ошибка обработки")

def main():
    application = Application.builder().token(BOT_TOKEN).build()    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    logger.info("Бот запущен...")
    application.run_polling()

if __name__ == "__main__":
    main()
