import os
import logging
import asyncio
from datetime import datetime
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes, CommandHandler

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Токен бота
BOT_TOKEN = "8253068855:AAFPNJke9PYju90RgZe4ZOKOuuMSJNAs0X8"

# Базы данных в памяти (как в Auto-Cloud API)
users_db = []
todos_db = []

async def process_message(message: str, user_id: int) -> str:
    """Обработка входящих сообщений"""
    message_lower = message.lower().strip()
    
    # 1. Приветствия - ДОБАВЛЕНО
    if any(word in message_lower for word in ['привет', 'hello', 'hi', 'start', 'начать', 'здравствуй', 'хай']):
        return "👋 Привет! Я бот для работы с Auto-Cloud API! 🚀\n\nНапишите 'помощь' для списка команд."
    
    # 2. Вопросы о возможностях - ДОБАВЛЕНО
    elif any(word in message_lower for word in ['что ты умеешь', 'что можешь', 'твои возможности', 'команды', 'функции']):
        return "🚀 Я умею работать с Auto-Cloud API:\n\n• 📊 Показывать статистику системы\n• 👥 Управлять пользователями\n• ✅ Управлять задачами\n• 🎯 Создавать новые записи\n\nНапишите 'помощь' для подробного списка команд."
    
    # 3. Помощь - ДОБАВЛЕНО
    elif any(word in message_lower for word in ['помощь', 'help', 'команды', 'справка']):
        return "📋 *Доступные команды:*\n\n" \
               "• `привет` - начать работу\n" \
               "• `помощь` - эта справка\n" \
               "• `статистика` - показать статистику системы\n" \
               "• `пользователи` - список всех пользователей\n" \
               "• `задачи` - список всех задач\n" \
               "• `создать пользователя Иван email@mail.ru`\n" \
               "• `создать задачу Заголовок Описание`\n\n" \
               "💡 Примеры:\n" \
               "`создать пользователя Алексей alex@company.com`\n" \
               "`создать задачу Разработка Создать новую функцию API`"
    
    # 4. Статистика системы
    elif any(word in message_lower for word in ['статистика', 'статус', 'stats', 'status']):
        return f"📊 *Статистика системы:*\n\n" \
               f"• 👥 Пользователей: {len(users_db)}\n" \
               f"• ✅ Задач: {len(todos_db)}\n" \
               f"• 🟢 Статус: Система работает"
    
    # 5. Пользователи
    elif any(word in message_lower for word in ['пользователи', 'users', 'юзеры', 'клиенты']):
        if not users_db:
            return "👥 *Пользователи:*\n\nПока нет пользователей в системе.\n\nИспользуйте: `создать пользователя Иван email@mail.ru`"
        
        users_list = "\n".join([f"• 👤 {u.get('username', 'N/A')} ({u.get('email', 'N/A')})" for u in users_db[:10]])
        return f"👥 *Пользователи ({len(users_db)}):*\n\n{users_list}" + \
               ("\n\n... и другие" if len(users_db) > 10 else "")
    
    # 6. Задачи
    elif any(word in message_lower for word in ['задачи', 'todos', 'таски', 'tasks', 'задания']):
        if not todos_db:
            return "✅ *Задачи:*\n\nПока нет задач в системе.\n\nИспользуйте: `создать задачу Заголовок Описание`"
        
        todos_list = "\n".join([f"• 📝 {t.get('title', 'N/A')}" for t in todos_db[:10]])
        return f"✅ *Задачи ({len(todos_db)}):*\n\n{todos_list}" + \
               ("\n\n... и другие" if len(todos_db) > 10 else "")
    
    # 7. Создание пользователя
    elif any(word in message_lower for word in ['создать пользователя', 'добавить пользователя', 'новый пользователь']):
        try:
            # Парсим сообщение
            parts = message.split(' ', 2)
            if len(parts) >= 3:
                username = parts[2].split(' ')[0]
                email = parts[2].split(' ')[1] if len(parts[2].split(' ')) > 1 else f"{username}@example.com"
                
                # Создаем пользователя
                user_data = {
                    "id": len(users_db) + 1,
                    "username": username,
                    "email": email,
                    "created_at": datetime.now().isoformat()
                }
                users_db.append(user_data)
                
                return f"✅ *Пользователь создан!*\n\n" \
                       f"👤 Имя: {username}\n" \
                       f"📧 Email: {email}\n" \
                       f"🆔 ID: {user_data['id']}\n" \
                       f"📅 Создан: {datetime.now().strftime('%d.%m.%Y %H:%M')}"
            else:
                return "❌ *Неверный формат!*\n\nИспользуйте: `создать пользователя Иван email@mail.ru`"
        except Exception as e:
            return f"❌ *Ошибка создания пользователя:*\n\n{str(e)}"
    
    # 8. Создание задачи
    elif any(word in message_lower for word in ['создать задачу', 'добавить задачу', 'новая задача']):
        try:
            # Парсим сообщение
            parts = message.split(' ', 2)
            if len(parts) >= 3:
                title = parts[2].split(' ', 1)[0]
                description = parts[2].split(' ', 1)[1] if len(parts[2].split(' ', 1)) > 1 else "Описание задачи"
                
                # Создаем задачу
                todo_data = {
                    "id": len(todos_db) + 1,
                    "title": title,
                    "description": description,
                    "created_at": datetime.now().isoformat()
                }
                todos_db.append(todo_data)
                
                return f"✅ *Задача создана!*\n\n" \
                       f"📝 Заголовок: {title}\n" \
                       f"📋 Описание: {description}\n" \
                       f"🆔 ID: {todo_data['id']}\n" \
                       f"📅 Создана: {datetime.now().strftime('%d.%m.%Y %H:%M')}"
            else:
                return "❌ *Неверный формат!*\n\nИспользуйте: `создать задачу Заголовок Описание задачи`"
        except Exception as e:
            return f"❌ *Ошибка создания задачи:*\n\n{str(e)}"
    
    # 9. Благодарности - ДОБАВЛЕНО
    elif any(word in message_lower for word in ['спасибо', 'благодарю', 'thanks', 'thank you']):
        return "😊 Пожалуйста! Рад помочь!\n\nЕсли нужна еще помощь - обращайтесь!"
    
    # 10. Прощания - ДОБАВЛЕНО
    elif any(word in message_lower for word in ['пока', 'до свидания', 'goodbye', 'see you']):
        return "👋 До свидания! Буду ра помочь снова!\n\nХорошего дня! 😊"
    
    # 11. Для всего остального
    else:
        return "❓ *Не понял команду*\n\nНапишите `помощь` для списка доступных команд или `привет` чтобы начать работу."

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик входящих сообщений"""
    try:
        user_message = update.message.text
        user_id = update.message.from_user.id
        
        logger.info(f"Получено сообщение от {user_id}: {user_message}")
        
        # Обрабатываем сообщение
        response = await process_message(user_message, user_id)
        
        # Отправляем ответ
        await update.message.reply_text(response, parse_mode='Markdown')
        
    except Exception as e:
        logger.error(f"Ошибка обработки сообщения: {e}")
        await update.message.reply_text("⚠️ *Произошла ошибка обработки.* Попробуйте еще раз")

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    await update.message.reply_text(
        "🚀 *Добро пожаловать в Auto-Cloud Bot!*\n\n"
        "Я ваш помощник для работы с системой управления пользователями и задачами!\n\n"
        "📋 *Для начала работы напишите:*\n"
        "• `привет` - начать общение\n"
        "• `помощь` - список команд\n"
        "• `статистика` - показать статистику\n\n"
        "💡 Я понимаю сообщения без слеша - просто напишите что вам нужно!",
        parse_mode='Markdown'
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /help"""
    await update.message.reply_text(
        "📋 *Доступные команды:*\n\n"
        "• `/start` - начать работу\n"
        "• `/help` - эта справка\n"
        "• `статистика` - показать статистику\n"
        "• `пользователи` - список пользователей\n"
        "• `задачи` - список задач\n"
        "• `создать пользователя Иван email@mail.ru`\n"
        "• `создать задачу Заголовок Описание`\n\n"
        "💡 *Примеры использования:*\n"
        "`создать пользователя Алексей alex@company.com`\n"
        "`создать задачу Разработка Создать новую функцию API`\n\n"
        "😊 Просто напишите команду без слеша!",
        parse_mode='Markdown'
    )

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик ошибок"""
    logger.error(f"Ошибка: {context.error}")

def main():
    """Запуск бота"""
    try:
        # Создаем приложение
        application = Application.builder().token(BOT_TOKEN).build()
        
        # Добавляем обработчики команд
        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(CommandHandler("help", help_command))
        
        # Добавляем обработчик текстовых сообщений
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        
        # Добавляем обработчик ошибок
        application.add_error_handler(error_handler)
        
        # Запускаем бота
        logger.info("Бот запущен и готов к работе...")
        print("✅ Бот успешно запущен!")
        print("📱 Теперь можете писать сообщения в Telegram")
        print("💬 Бот понимает: привет, помощь, статистика, пользователи, задачи и др.")
        
        application.run_polling()
        
    except Exception as e:
        logger.error(f"Ошибка запуска бота: {e}")
        print(f"❌ Ошибка запуска: {e}")

if __name__ == "__main__":
    main()
