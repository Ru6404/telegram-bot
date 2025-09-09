import os
import sqlite3
import logging
from datetime import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class UniversalBot:
    def __init__(self):
        self.token = "8253068855:AAFPNJke9PYju90RgZe4ZOKOuuMSJNAs0X8"
        if not self.token:
            raise ValueError("BOT_TOKEN not found!")
        
        self.application = Application.builder().token(self.token).build()
        self.scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
        self.setup_handlers()
        self.init_database()
    
    def init_database(self):
        """Инициализация базы данных"""
        try:
            self.conn = sqlite3.connect('bot_database.db', check_same_thread=False)
            self.cursor = self.conn.cursor()
            
            # Создание таблиц
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER UNIQUE,
                    username TEXT,
                    first_name TEXT,
                    last_name TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    message TEXT,
                    response TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Добавляем тестовые данные
            self.cursor.execute('''
                INSERT OR IGNORE INTO users (user_id, username, first_name, last_name)
                VALUES (?, ?, ?, ?)
            ''', (999999, 'system', 'System', 'User'))
            
            self.conn.commit()
            print("✅ База данных успешно инициализирована")
            
        except Exception as e:
            print(f"❌ Ошибка при создании базы данных: {e}")
            # Создаем файл базы данных вручную
            try:
                with open('bot_database.db', 'w') as f:
                    pass
                print("✅ Файл базы данных создан вручную")
                # Повторная инициализация
                self.init_database()
            except Exception as e2:
                print(f"❌ Не удалось создать файл базы: {e2}")
    
    def save_user(self, user_data):
        """Сохранение пользователя в базу данных"""
        try:
            self.cursor.execute('''
                INSERT OR IGNORE INTO users (user_id, username, first_name, last_name)
                VALUES (?, ?, ?, ?)
            ''', (user_data.id, user_data.username, user_data.first_name, user_data.last_name))
            self.conn.commit()
        except Exception as e:
            logger.error(f"Error saving user: {e}")
    
    def save_message(self, user_id, message, response):
        """Сохранение сообщения в базу данных"""
        try:
            self.cursor.execute('''
                INSERT INTO messages (user_id, message, response)
                VALUES (?, ?, ?)
            ''', (user_id, message, response))
            self.conn.commit()
        except Exception as e:
            logger.error(f"Error saving message: {e}")
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /start"""
        user = update.message.from_user
        self.save_user(user)
        
        welcome_text = """
        🤖 Привет! Я универсальный бот-ассистент.
        
        Я могу:
        • Отвечать на вопросы
        • Решать математические задачи
        • Предоставлять информацию
        • И многое другое!
        
        Просто напишите мне что-нибудь!
        """
        
        await update.message.reply_text(welcome_text)
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик всех текстовых сообщений"""
        try:
            user = update.message.from_user
            user_message = update.message.text
            
            self.save_user(user)
            
            # Обработка сообщения
            response = await self.process_message(user_message, user.id)
            
            # Сохранение в базу данных
            self.save_message(user.id, user_message, response)
            
            await update.message.reply_text(response)
            
        except Exception as e:
            logger.error(f"Error handling message: {e}")
            await update.message.reply_text("⚠️ Произошла ошибка при обработке запроса")
    
    async def process_message(self, message: str, user_id: int) -> str:
        """Обработка входящего сообщения"""
        message_lower = message.lower()
        
        # Простая логика обработки
        if any(word in message_lower for word in ['привет', 'hello', 'hi', 'start']):
            return "Привет! Чем могу помочь?"
        
        elif any(word in message_lower for word in ['погода', 'weather']):
            return "Для получения погоды мне нужен API ключ от погодного сервиса"
        
        elif any(word in message_lower for word in ['калькулятор', 'посчитай', 'сколько будет']):
            try:
                # Простой калькулятор
                clean_msg = message_lower.replace('посчитай', '').replace('калькулятор', '').replace('сколько будет', '').strip()
                result = eval(clean_msg)
                return f"📊 Результат: {result}"
            except:
                return "❌ Не могу вычислить выражение"
        
        else:
            return "🤔 Интересный вопрос! Пока я умею отвечать на простые запросы. Развиваюсь!"
    
    def setup_handlers(self):
        """Настройка обработчиков команд"""
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
    
    def run(self):
        """Запуск бота"""
        logger.info("Бот запускается...")
        self.scheduler.start()
        self.application.run_polling()
    
    def __del__(self):
        """Закрытие соединения с БД при завершении"""
        if hasattr(self, 'conn'):
            self.conn.close()

if __name__ == "__main__":
    try:
        bot = UniversalBot()
        bot.run()
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
