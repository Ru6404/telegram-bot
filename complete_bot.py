import os
import logging
import httpx
import uuid
from datetime import datetime
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes, CommandHandler, CallbackContext

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Токен бота
BOT_TOKEN = "8253068855:AAFPNJke9PYju90RgZe4ZOKOuuMSJNAs0X8"

# Ваш Auto-Cloud API
API_URL = "http://localhost:8000"

class AutoCloudClient:
    """Полный клиент для вашего Auto-Cloud API"""
    
    def __init__(self):
        self.base_url = API_URL
        self.session = httpx.AsyncClient(timeout=30.0)
    
    async def api_request(self, method: str, endpoint: str, data: dict = None):
        """Универсальный запрос к вашему API"""
        try:
            url = f"{self.base_url}{endpoint}"
            if method == "GET":
                response = await self.session.get(url)
            elif method == "POST":
                response = await self.session.post(url, json=data)
            elif method == "PUT":
                response = await self.session.put(url, json=data)
            elif method == "DELETE":
                response = await self.session.delete(url)
            
            return response.json() if response.status_code == 200 else None
            
        except Exception as e:
            logger.error(f"API Error: {e}")
            return None
    
    # Users endpoints
    async def get_users(self):
        return await self.api_request("GET", "/users")
    
    async def create_user(self, username: str, email: str):
        return await self.api_request("POST", "/users", {"username": username, "email": email})
    
    async def delete_user(self, user_id: str):
        return await self.api_request("DELETE", f"/users/{user_id}")
    
    # Todos endpoints  
    async def get_todos(self):
        return await self.api_request("GET", "/todos")
    
    async def create_todo(self, title: str, description: str):
        return await self.api_request("POST", "/todos", {"title": title, "description": description})
    
    async def delete_todo(self, todo_id: str):
        return await self.api_request("DELETE", f"/todos/{todo_id}")
    
    # System endpoints
    async def get_stats(self):
        return await self.api_request("GET", "/")
    
    async def get_health(self):
        return await self.api_request("GET", "/health")

# Глобальный клиент
api = AutoCloudClient()

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /start - входная точка"""
    await update.message.reply_text(
        "🚀 *Добро пожаловать в Auto-Cloud System!*\n\n"
        "Я - полноценный интерфейс вашей промышленной схемы!\n\n"
        "📋 *Возможности:*\n"
        "• Полное управление пользователями\n"
        "• Полное управление задачами\n"
        "• Мониторинг системы\n"
        "• Работа с вашим API\n\n"
        "Напишите `меню` для доступа ко всем функциям!",
        parse_mode='Markdown'
    )

async def menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Главное меню системы"""
    await update.message.reply_text(
        "🏢 *Auto-Cloud System Menu*\n\n"
        "👥 *Пользователи:*\n"
        "• `пользователи` - список\n"
        "• `добавить пользователя Иван email@mail.ru`\n"
        "• `удалить пользователя ID`\n\n"
        "✅ *Задачи:*\n"
        "• `задачи` - список\n"
        "• `добавить задачу Заголовок Описание`\n"
        "• `удалить задачу ID`\n\n"
        "📊 *Система:*\n"
        "• `статус` - состояние системы\n"
        "• `статистика` - метрики\n\n"
        "⚙️ *API:*\n"
        "• `api статус` - здоровье API\n"
        "• `api документация` - ссылки",
        parse_mode='Markdown'
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик всех сообщений"""
    message = update.message.text
    message_lower = message.lower()
    
    try:
        # 1. Системные команды
        if message_lower in ['меню', 'menu', 'команды']:
            await menu_command(update, context)
            return
        
        elif message_lower in ['статус', 'status', 'здоровье']:
            health = await api.get_health()
            if health:
                await update.message.reply_text(f"🟢 *Система работает:*\n\n{health}", parse_mode='Markdown')
            else:
                await update.message.reply_text("🔴 *API недоступен!* Запустите `python main.py`", parse_mode='Markdown')
            return
        
        elif message_lower in ['статистика', 'stats']:
            users = await api.get_users()
            todos = await api.get_todos()
            stats = await api.get_stats()
            
            response = f"📊 *Статистика системы:*\n\n"
            response += f"👥 Пользователей: {len(users) if users else 0}\n"
            response += f"✅ Задач: {len(todos) if todos else 0}\n"
            response += f"🏢 API: {'🟢 Работает' if stats else '🔴 Недоступен'}"
            
            await update.message.reply_text(response, parse_mode='Markdown')
            return
        
        # 2. Пользователи
        elif message_lower == 'пользователи':
            users = await api.get_users()
            if not users:
                await update.message.reply_text("👥 *Пользователи:*\n\nНет пользователей", parse_mode='Markdown')
                return
            
            users_list = "\n".join([f"• 👤 {u['username']} ({u['email']}) - ID: {u['id']}" for u in users[:10]])
            await update.message.reply_text(f"👥 *Пользователи ({len(users)}):*\n\n{users_list}", parse_mode='Markdown')
            return
        
        elif message_lower.startswith('добавить пользователя'):
            try:
                _, _, data = message.split(' ', 2)
                username, email = data.split(' ', 1)
                
                result = await api.create_user(username.strip(), email.strip())
                if result:
                    await update.message.reply_text(
                        f"✅ *Пользователь создан!*\n\n"
                        f"👤 Имя: {result['username']}\n"
                        f"📧 Email: {result['email']}\n"
                        f"🆔 ID: {result['id']}",
                        parse_mode='Markdown'
                    )
                else:
                    await update.message.reply_text("❌ *Ошибка создания пользователя!*", parse_mode='Markdown')
            except:
                await update.message.reply_text("❌ Формат: `добавить пользователя Иван email@mail.ru`", parse_mode='Markdown')
            return
        
        elif message_lower.startswith('удалить пользователя'):
            try:
                _, _, user_id = message.split(' ', 2)
                result = await api.delete_user(user_id.strip())
                if result:
                    await update.message.reply_text(f"✅ Пользователь {user_id} удален!", parse_mode='Markdown')
                else:
                    await update.message.reply_text("❌ Ошибка удаления!", parse_mode='Markdown')
            except:
                await update.message.reply_text("❌ Формат: `удалить пользователя ID`", parse_mode='Markdown')
            return
        
        # 3. Задачи
        elif message_lower == 'задачи':
            todos = await api.get_todos()
            if not todos:
                await update.message.reply_text("✅ *Задачи:*\n\nНет задач", parse_mode='Markdown')
                return
            
            todos_list = "\n".join([f"• 📝 {t['title']} - ID: {t['id']}" for t in todos[:10]])
            await update.message.reply_text(f"✅ *Задачи ({len(todos)}):*\n\n{todos_list}", parse_mode='Markdown')
            return
        
        elif message_lower.startswith('добавить задачу'):
            try:
                _, _, data = message.split(' ', 2)
                title, description = data.split(' ', 1)
                
                result = await api.create_todo(title.strip(), description.strip())
                if result:
                    await update.message.reply_text(
                        f"✅ *Задача создана!*\n\n"
                        f"📝 Заголовок: {result['title']}\n"
                        f"📋 Описание: {result['description']}\n"
                        f"🆔 ID: {result['id']}",
                        parse_mode='Markdown'
                    )
                else:
                    await update.message.reply_text("❌ *Ошибка создания задачи!*", parse_mode='Markdown')
            except:
                await update.message.reply_text("❌ Формат: `добавить задачу Заголовок Описание`", parse_mode='Markdown')
            return
        
        elif message_lower.startswith('удалить задачу'):
            try:
                _, _, todo_id = message.split(' ', 2)
                result = await api.delete_todo(todo_id.strip())
                if result:
                    await update.message.reply_text(f"✅ Задача {todo_id} удалена!", parse_mode='Markdown')
                else:
                    await update.message.reply_text("❌ Ошибка удаления!", parse_mode='Markdown')
            except:
                await update.message.reply_text("❌ Формат: `удалить задачу ID`", parse_mode='Markdown')
            return
        
        # 4. API управление
        elif message_lower == 'api статус':
            health = await api.get_health()
            stats = await api.get_stats()
            
            response = "🌐 *API Status:*\n\n"
            response += f"• Health: {'🟢 OK' if health else '🔴 Down'}\n"
            response += f"• Stats: {'🟢 Available' if stats else '🔴 Unavailable'}\n"
            response += f"• Endpoint: {API_URL}"
            
            await update.message.reply_text(response, parse_mode='Markdown')
            return
        
        elif message_lower == 'api документация':
            await update.message.reply_text(
                "📚 *API Documentation:*\n\n"
                f"• Swagger: {API_URL}/docs\n"
                f"• Redoc: {API_URL}/redoc\n"
                f"• OpenAPI: {API_URL}/openapi.json",
                parse_mode='Markdown'
            )
            return
        
        # 5. Неизвестная команда
        else:
            await update.message.reply_text(
                "❓ *Неизвестная команда*\n\n"
                "Напишите `меню` для списка всех команд системы\n"
                "Или `статус` для проверки состояния",
                parse_mode='Markdown'
            )
            
    except Exception as e:
        logger.error(f"Error: {e}")
        await update.message.reply_text("⚠️ *System Error!* Попробуйте позже.", parse_mode='Markdown')

def main():
    """Запуск полной системы"""
    try:
        application = Application.builder().token(BOT_TOKEN).build()
        
        # Команды
        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(CommandHandler("menu", menu_command))
        application.add_handler(CommandHandler("help", menu_command))
        
        # Текстовые сообщения
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        
        logger.info("🏢 Auto-Cloud System Bot запущен!")
        print("✅ Полная система активирована!")
        print("📱 Бот теперь ПОЛНЫЙ интерфейс вашей схемы!")
        print("🌐 API: http://localhost:8000")
        print("📚 Docs: http://localhost:8000/docs")
        
        application.run_polling()
        
    except Exception as e:
        logger.error(f"Startup Error: {e}")
        print(f"❌ Ошибка запуска: {e}")

if __name__ == "__main__":
    main()
