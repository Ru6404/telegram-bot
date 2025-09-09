import os
import logging
import asyncio
import httpx
import os
import logging
import httpx
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

# Конфигурация Auto-Cloud API (ВАША СХЕМА)
AUTO_CLOUD_API_URL = "http://localhost:8000"

class AutoCloudAPI:
    """Класс для работы с вашим Auto-Cloud API"""
    
    def __init__(self, base_url: str = AUTO_CLOUD_API_URL):
        self.base_url = base_url
        
    async def get_users(self):
        """Получить пользователей из вашего API"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/users", timeout=10.0)
                return response.json()
        except Exception as e:
            logger.error(f"Ошибка подключения к API: {e}")
            return None
    
    async def create_user(self, username: str, email: str):
        """Создать пользователя через ваш API"""
        try:
            async with httpx.AsyncClient() as client:
                data = {"username": username, "email": email}
                response = await client.post(f"{self.base_url}/users", json=data, timeout=10.0)
                return response.json()
        except Exception as e:
            logger.error(f"Ошибка создания пользователя: {e}")
            return None
    
    async def get_todos(self):
        """Получить задачи из вашего API"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/todos", timeout=10.0)
                return response.json()
        except Exception as e:
            logger.error(f"Ошибка получения задач: {e}")
            return None
    
    async def create_todo(self, title: str, description: str):
        """Создать задачу через ваш API"""
        try:
            async with httpx.AsyncClient() as client:
                data = {"title": title, "description": description}
                response = await client.post(f"{self.base_url}/todos", json=data, timeout=10.0)
                return response.json()
        except Exception as e:
            logger.error(f"Ошибка создания задачи: {e}")
            return None

# Создаем экземпляр API (ПОДКЛЮЧЕНИЕ К ВАШЕЙ СХЕМЕ)
api_client = AutoCloudAPI()

async def process_message(message: str, user_id: int) -> str:
    """Обработка сообщений с интеграцией в вашу схему"""
    message_lower = message.lower().strip()
    
    # 1. Приветствия
    if any(word in message_lower for word in ['привет', 'hello', 'hi', 'start', 'начать']):
        return "👋 Привет! Я бот, интегрированный с вашей Auto-Cloud API схемой! 🚀"
    
    # 2. Помощь
    elif any(word in message_lower for word in ['помощь', 'help', 'команды']):
        return "📋 *Команды интегрированные с Auto-Cloud API:*\n\n" \
               "• `статистика` - статистика системы\n" \
               "• `пользователи` - список пользователей\n" \
               "• `задачи` - список задач\n" \
               "• `создать пользователя Иван email@mail.ru`\n" \
               "• `создать задачу Заголовок Описание`"
    
    # 3. Статистика (ИЗ ВАШЕГО API)
    elif any(word in message_lower for word in ['статистика', 'статус']):
        users = await api_client.get_users()
        todos = await api_client.get_todos()
        
        if users is None or todos is None:
            return "❌ *Ошибка подключения к Auto-Cloud API!*\n\nЗапустите: `python main.py`"
        
        return f"📊 *Статистика из вашей схемы:*\n\n" \
               f"• 👥 Пользователей: {len(users)}\n" \
               f"• ✅ Задач: {len(todos)}\n" \
               f"• 🏢 Auto-Cloud API: Работает"
    
    # 4. Пользователи (ИЗ ВАШЕГО API)
    elif any(word in message_lower for word in ['пользователи', 'users']):
        users = await api_client.get_users()
        
        if users is None:
            return "❌ *Ошибка подключения к API!* Запустите ваш FastAPI сервер."
        
        if not users:
            return "👥 *Пользователи из вашей схемы:*\n\nПока нет пользователей"
        
        users_list = "\n".join([f"• 👤 {u.get('username', 'N/A')} ({u.get('email', 'N/A')})" for u in users[:5]])
        return f"👥 *Пользователи из вашей схемы ({len(users)}):*\n\n{users_list}"
    
    # 5. Задачи (ИЗ ВАШЕГО API)
    elif any(word in message_lower for word in ['задачи', 'todos']):
        todos = await api_client.get_todos()
        
        if todos is None:
            return "❌ *Ошибка подключения к API!* Запустите ваш FastAPI сервер."
        
        if not todos:
            return "✅ *Задачи из вашей схемы:*\n\nПока нет задач"
        
        todos_list = "\n".join([f"• 📝 {t.get('title', 'N/A')}" for t in todos[:5]])
        return f"✅ *Задачи из вашей схемы ({len(todos)}):*\n\n{todos_list}"
    
    # 6. Создание пользователя (ЧЕРЕЗ ВАШ API)
    elif any(word in message_lower for word in ['создать пользователя', 'добавить пользователя']):
        try:
            parts = message.split(' ', 2)
            if len(parts) >= 3:
                username = parts[2].split(' ')[0]
                email = parts[2].split(' ')[1] if len(parts[2].split(' ')) > 1 else f"{username}@example.com"
                
                # ИСПОЛЬЗУЕМ ВАШ API
                result = await api_client.create_user(username, email)
                
                if result is None:
                    return "❌ *Ошибка создания!* Проверьте ваш API сервер."
                
                return f"✅ *Пользователь создан через ваш API!*\n\n" \
                       f"👤 Имя: {result.get('username', 'N/A')}\n" \
                       f"📧 Email: {result.get('email', 'N/A')}\n" \
                       f"🆔 ID: {result.get('id', 'N/A')}"
        except:
            return "❌ Используйте: 'создать пользователя Иван email@mail.ru'"
    
    # 7. Создание задачи (ЧЕРЕЗ ВАШ API)
    elif any(word in message_lower for word in ['создать задачу', 'добавить задачу']):
        try:
            parts = message.split(' ', 2)
            if len(parts) >= 3:
                title = parts[2].split(' ', 1)[0]
                description = parts[2].split(' ', 1)[1] if len(parts[2].split(' ', 1)) > 1 else "Описание"
                
                # ИСПОЛЬЗУЕМ ВАШ API
                result = await api_client.create_todo(title, description)
                
                if result is None:
                    return "❌ *Ошибка создания!* Проверьте ваш API сервер."
                
                return f"✅ *Задача создана через ваш API!*\n\n" \
                       f"📝 Заголовок: {result.get('title', 'N/A')}\n" \
                       f"📋 Описание: {result.get('description', 'N/A')}\n" \
                       f"🆔 ID: {result.get('id', 'N/A')}"
        except:
            return "❌ Используйте: 'создать задачу Заголовок Описание'"
    
    # 8. Для всего остального
    else:
        return "❓ Напишите 'помощь' для списка команд"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик сообщений"""
    try:
        response = await process_message(update.message.text, update.message.from_user.id)
        await update.message.reply_text(response, parse_mode='Markdown')
    except Exception as e:
        logger.error(f"Ошибка: {e}")
        await update.message.reply_text("⚠️ Ошибка обработки")

def main():
    """Запуск бота"""
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    logger.info("🤖 Бот запущен и интегрирован с Auto-Cloud API")
    print("✅ Бот подключен к вашей схеме!")
    application.run_polling()

if __name__ == "__main__":
    main()
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

# Конфигурация Auto-Cloud API
AUTO_CLOUD_API_URL = "http://localhost:8000"

class AutoCloudAPI:
    def __init__(self, base_url: str = AUTO_CLOUD_API_URL):
        self.base_url = base_url
        
    async def get_users(self):
        """Получить всех пользователей"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/users", timeout=10.0)
                return response.json()
        except Exception as e:
            logger.error(f"Ошибка получения пользователей: {e}")
            return []
    
    async def create_user(self, username: str, email: str):
        """Создать нового пользователя"""
        try:
            async with httpx.AsyncClient() as client:
                data = {"username": username, "email": email}
                response = await client.post(f"{self.base_url}/users", json=data, timeout=10.0)
                return response.json()
        except Exception as e:
            logger.error(f"Ошибка создания пользователя: {e}")
            return {"error": str(e)}
    
    async def get_todos(self):
        """Получить все задачи"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/todos", timeout=10.0)
                return response.json()
        except Exception as e:
            logger.error(f"Ошибка получения задач: {e}")
            return []
    
    async def create_todo(self, title: str, description: str):
        """Создать новую задачу"""
        try:
            async with httpx.AsyncClient() as client:
                data = {"title": title, "description": description}
                response = await client.post(f"{self.base_url}/todos", json=data, timeout=10.0)
                return response.json()
        except Exception as e:
            logger.error(f"Ошибка создания задачи: {e}")
            return {"error": str(e)}
    
    async def get_stats(self):
        """Получить статистику"""
        try:
            users = await self.get_users()
            todos = await self.get_todos()
            
            return {
                "users_count": len(users),
                "todos_count": len(todos),
                "status": "online"
            }
        except Exception as e:
            logger.error(f"Ошибка получения статистики: {e}")
            return {"error": str(e)}

# Создаем экземпляр API
auto_cloud_api = AutoCloudAPI()

async def process_message(message: str, user_id: int) -> str:
    """Обработка входящих сообщений для Auto-Cloud API"""
    message_lower = message.lower().strip()
    
    # 1. Статистика системы
    if any(word in message_lower for word in ['статистика', 'статус', 'stats', 'status']):
        stats = await auto_cloud_api.get_stats()
        if isinstance(stats, dict) and 'error' in stats:
            return "❌ *Ошибка подключения к API!*\n\nПроверьте, запущен ли Auto-Cloud API на localhost:8000"
        
        return f"📊 *Статистика Auto-Cloud API:*\n\n" \
               f"• 👥 Пользователей: {stats.get('users_count', 0)}\n" \
               f"• ✅ Задач: {stats.get('todos_count', 0)}\n" \
               f"• 🟢 Статус: {stats.get('status', 'online')}"
    
    # 2. Пользователи
    elif any(word in message_lower for word in ['пользователи', 'users', 'юзеры']):
        users = await auto_cloud_api.get_users()
        if not users:
            return "👥 *Пользователи:*\n\nНет пользователей в системе"
        
        users_list = "\n".join([f"• 👤 {user.get('username', 'N/A')} ({user.get('email', 'N/A')})" for user in users[:10]])
        return f"👥 *Пользователи ({len(users)}):*\n\n{users_list}"
    
    # 3. Задачи
    elif any(word in message_lower for word in ['задачи', 'todos', 'таски', 'tasks']):
        todos = await auto_cloud_api.get_todos()
        if not todos:
            return "✅ *Задачи:*\n\nНет задач в системе"
        
        todos_list = "\n".join([f"• 📝 {todo.get('title', 'N/A')}" for todo in todos[:10]])
        return f"✅ *Задачи ({len(todos)}):*\n\n{todos_list}"
    
    # 4. Создание пользователя
    elif any(word in message_lower for word in ['создать пользователя', 'добавить пользователя', 'новый пользователь']):
        parts = message.split(' ', 2)
        if len(parts) >= 3:
            try:
                # Парсим "создать пользователя Иван email@example.com"
                username = parts[2].split(' ')[0]
                email = parts[2].split(' ')[1] if len(parts[2].split(' ')) > 1 else f"{username}@example.com"
                
                result = await auto_cloud_api.create_user(username, email)
                if 'error' in result:
                    return f"❌ *Ошибка создания пользователя:*\n\n{result['error']}"
                
                return f"✅ *Пользователь создан!*\n\n" \
                       f"👤 Имя: {result.get('username', 'N/A')}\n" \
                       f"📧 Email: {result.get('email', 'N/A')}\n" \
                       f"🆔 ID: {result.get('id', 'N/A')}"
            except Exception as e:
                return f"❌ *Ошибка формата:*\n\nИспользуйте: 'создать пользователя Иван email@example.com'"
        else:
            return "👤 *Создание пользователя:*\n\nИспользуйте формат:\n`создать пользователя Иван email@example.com`"
    
    # 5. Создание задачи
    elif any(word in message_lower for word in ['создать задачу', 'добавить задачу', 'новая задача']):
        parts = message.split(' ', 2)
        if len(parts) >= 3:
            try:
                # Парсим "создать задачу Заголовок Описание задачи"
                title = parts[2].split(' ', 1)[0]
                description = parts[2].split(' ', 1)[1] if len(parts[2].split(' ', 1)) > 1 else "Описание отсутствует"
                
                result = await auto_cloud_api.create_todo(title, description)
                if 'error' in result:
                    return f"❌ *Ошибка создания задачи:*\n\n{result['error']}"
                
                return f"✅ *Задача создана!*\n\n" \
                       f"📝 Заголовок: {result.get('title', 'N/A')}\n" \
                       f"📋 Описание: {result.get('description', 'N/A')}\n" \
                       f"🆔 ID: {result.get('id', 'N/A')}"
            except Exception as e:
                return f"❌ *Ошибка формата:*\n\nИспользуйте: 'создать задачу Заголовок Описание задачи'"
        else:
            return "✅ *Создание задачи:*\n\nИспользуйте формат:\n`создать задачу Заголовок Описание задачи`"
    
    # 6. Помощь
    elif any(word in message_lower for word in ['помощь', 'help', 'команды', 'что ты умеешь']):
        return "🚀 *Auto-Cloud Bot Команды:*\n\n" \
               "• `статистика` - показать статистику системы\n" \
               "• `пользователи` - список пользователей\n" \
               "• `задачи` - список задач\n" \
               "• `создать пользователя Иван email@example.com` - создать пользователя\n" \
               "• `создать задачу Заголовок Описание` - создать задачу\n\n" \
               "📊 *Auto-Cloud API должен быть запущен на localhost:8000*"
    
    # 7. Приветствие
    elif any(word in message_lower for word in ['привет', 'hello', 'start', 'начать']):
        return "🚀 *Добро пожаловать в Auto-Cloud Bot!*\n\n" \
               "Я помогу вам управлять вашей Auto-Cloud API через Telegram!\n\n" \
               "Напишите `помощь` для списка команд."
    
    # 8. Неизвестная команда
    else:
        return "❓ *Неизвестная команда*\n\n" \
               "Напишите `помощь` для списка доступных команд."

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик входящих сообщений"""
    try:
        user_message = update.message.text
        user_id = update.message.from_user.id
        
        logger.info(f"Получено сообщение от {user_id}: {user_message}")
        
        response = await process_message(user_message, user_id)
        await update.message.reply_text(response, parse_mode='Markdown')
        
    except Exception as e:
        logger.error(f"Ошибка обработки сообщения: {e}")
        await update.message.reply_text("⚠️ *Произошла ошибка обработки.* Попробуйте еще раз")

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    await update.message.reply_text(
        "🚀 *Добро пожаловать в Auto-Cloud Bot!*\n\n"
        "Я ваш помощник для работы с Auto-Cloud API через Telegram!\n\n"
        "📋 *Доступные команды:*\n"
        "• /start - Начать работу\n"
        "• /help - Помощь и команды\n"
        "• /stats - Статистика системы\n"
        "• /users - Список пользователей\n"
        "• /todos - Список задач\n\n"
        "Просто напишите мне команду или сообщение!",
        parse_mode='Markdown'
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /help"""
    await update.message.reply_text(
        "📋 *Команды Auto-Cloud Bot:*\n\n"
        "• /start - Начать работу\n"
        "• /help - Эта справка\n"
        "• /stats - Статистика системы\n"
        "• /users - Список пользователей\n"
        "• /todos - Список задач\n\n"
        "📝 *Текстовые команды:*\n"
        "• `статистика` - показать статистику\n"
        "• `пользователи` - список пользователей\n"
        "• `задачи` - список задач\n"
        "• `создать пользователя Иван email@example.com`\n"
        "• `создать задачу Заголовок Описание`\n\n"
        "📊 *Auto-Cloud API должен быть запущен на localhost:8000*",
        parse_mode='Markdown'
    )

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /stats"""
    stats = await auto_cloud_api.get_stats()
    if isinstance(stats, dict) and 'error' in stats:
        await update.message.reply_text("❌ *Ошибка подключения к API!*\n\nПроверьте, запущен ли Auto-Cloud API", parse_mode='Markdown')
    else:
        await update.message.reply_text(
            f"📊 *Статистика Auto-Cloud API:*\n\n"
            f"• 👥 Пользователей: {stats.get('users_count', 0)}\n"
            f"• ✅ Задач: {stats.get('todos_count', 0)}\n"
            f"• 🟢 Статус: {stats.get('status', 'online')}",
            parse_mode='Markdown'
        )

async def users_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /users"""
    users = await auto_cloud_api.get_users()
    if not users:
        await update.message.reply_text("👥 *Пользователи:*\n\nНет пользователей в системе", parse_mode='Markdown')
    else:
        users_list = "\n".join([f"• 👤 {user.get('username', 'N/A')} ({user.get('email', 'N/A')})" for user in users[:15]])
        await update.message.reply_text(f"👥 *Пользователи ({len(users)}):*\n\n{users_list}", parse_mode='Markdown')

async def todos_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /todos"""
    todos = await auto_cloud_api.get_todos()
    if not todos:
        await update.message.reply_text("✅ *Задачи:*\n\nНет задач в системе", parse_mode='Markdown')
    else:
        todos_list = "\n".join([f"• 📝 {todo.get('title', 'N/A')}" for todo in todos[:15]])
        await update.message.reply_text(f"✅ *Задачи ({len(todos)}):*\n\n{todos_list}", parse_mode='Markdown')

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик ошибок"""
    logger.error(f"Ошибка: {context.error}")

def main():
    """Запуск бота"""
    try:
        application = Application.builder().token(BOT_TOKEN).build()
        
        # Добавляем обработчики команд
        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("stats", stats_command))
        application.add_handler(CommandHandler("users", users_command))
        application.add_handler(CommandHandler("todos", todos_command))
        
        # Добавляем обработчик текстовых сообщений
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        
        # Добавляем обработчик ошибок
        application.add_error_handler(error_handler)
        
        logger.info("🤖 Auto-Cloud Bot запущен и готов к работе...")
        print("✅ Auto-Cloud Bot успешно запущен!")
        print("📊 Бот интегрирован с Auto-Cloud API")
        print("📱 Теперь можете писать команды в Telegram")
        
        application.run_polling()
        
    except Exception as e:
        logger.error(f"Ошибка запуска бота: {e}")
        print(f"❌ Ошибка запуска: {e}")

if __name__ == "__main__":
    main()
