import logging
import os
import sqlite3
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
from datetime import datetime, timedelta
import json

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Конфигурация
BOT_TOKEN = "8253068855:AAFPNJke9PYju90RgZe4ZOKOuuMSJNAs0X8"
ADMIN_ID = 5569793273

# Инициализация базы данных
def init_db():
    conn = sqlite3.connect('clients.db')
    cursor = conn.cursor()
    
    # Таблица клиентов
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS clients (
        id INTEGER PRIMARY KEY,
        telegram_id INTEGER UNIQUE,
        name TEXT,
        username TEXT,
        phone TEXT,
        email TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Таблица задач
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY,
        client_id INTEGER,
        title TEXT,
        description TEXT,
        status TEXT DEFAULT 'новый',
        priority TEXT DEFAULT 'средний',
        assigned_to INTEGER,
        deadline DATETIME,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (client_id) REFERENCES clients (id),
        FOREIGN KEY (assigned_to) REFERENCES clients (id)
    )
    ''')
    
    # Таблица сообщений
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY,
        client_id INTEGER,
        message_text TEXT,
        is_from_client BOOLEAN,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (client_id) REFERENCES clients (id)
    )
    ''')
    
    # Таблица заказов
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY,
        client_id INTEGER,
        order_number TEXT,
        description TEXT,
        status TEXT DEFAULT 'в обработке',
        amount REAL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (client_id) REFERENCES clients (id)
    )
    ''')
    
    conn.commit()
    conn.close()

# Меню для разных пользователей
ADMIN_MENU = [
    ['📊 Все задачи', '👥 Все клиенты'],
    ['📦 Все заказы', '📨 Рассылка'],
    ['📈 Статистика', '⚙️ Настройки']
]

CLIENT_MENU = [
    ['📋 Мои задачи', '📦 Мои заказы'],
    ['📞 Контакты', '💬 Написать'],
    ['🔄 Статус заказа']
]

admin_markup = ReplyKeyboardMarkup(ADMIN_MENU, resize_keyboard=True)
client_markup = ReplyKeyboardMarkup(CLIENT_MENU, resize_keyboard=True)

# ==================== БАЗА ДАННЫХ ==================== #

def get_db_connection():
    return sqlite3.connect('clients.db')

def register_client(user_id, first_name, last_name, username):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT OR IGNORE INTO clients (telegram_id, name, username)
    VALUES (?, ?, ?)
    ''', (user_id, f"{first_name} {last_name}", username))
    
    conn.commit()
    conn.close()

def add_task(client_id, title, description, priority='средний'):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO tasks (client_id, title, description, priority)
    VALUES (?, ?, ?, ?)
    ''', (client_id, title, description, priority))
    
    task_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return task_id

def add_message(client_id, message_text, is_from_client=True):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO messages (client_id, message_text, is_from_client)
    VALUES (?, ?, ?)
    ''', (client_id, message_text, is_from_client))
    
    conn.commit()
    conn.close()

def add_order(client_id, order_number, description, amount=0):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO orders (client_id, order_number, description, amount)
    VALUES (?, ?, ?, ?)
    ''', (client_id, order_number, description, amount))
    
    conn.commit()
    conn.close()

# ==================== АДМИНСКИЕ ФУНКЦИИ ==================== #

async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) FROM clients')
    clients_count = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM tasks WHERE status != "завершено"')
    tasks_count = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM messages WHERE is_from_client = 1 AND created_at > datetime("now", "-1 day")')
    new_messages = cursor.fetchone()[0]
    
    conn.close()
    
    text = (
        "👨‍💼 <b>Админ-панель</b>\n\n"
        "📊 <b>Статистика:</b>\n"
        f"• Клиентов: {clients_count}\n"
        f"• Активных задач: {tasks_count}\n"
        f"• Новых сообщений (24ч): {new_messages}\n\n"
        "Выберите действие:"
    )
    await update.message.reply_text(text, reply_markup=admin_markup, parse_mode='HTML')

async def show_all_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT t.id, t.title, t.status, t.priority, c.name 
    FROM tasks t 
    JOIN clients c ON t.client_id = c.id 
    WHERE t.status != "завершено"
    ORDER BY t.created_at DESC
    ''')
    
    tasks = cursor.fetchall()
    conn.close()
    
    if not tasks:
        await update.message.reply_text("📝 Нет активных задач.")
        return
    
    text = "📊 <b>Все активные задачи:</b>\n\n"
    for task in tasks:
        text += f"• #{task[0]}: {task[1]}\n"
        text += f"  👤 {task[4]}\n"
        text += f"  🚦 {task[2]} | ⚡ {task[3]}\n\n"
    
    await update.message.reply_text(text, parse_mode='HTML')

async def show_all_clients(update: Update, context: ContextTypes.DEFAULT_TYPE):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT c.telegram_id, c.name, c.username, 
           COUNT(t.id) as task_count,
           COUNT(m.id) as message_count
    FROM clients c
    LEFT JOIN tasks t ON c.id = t.client_id
    LEFT JOIN messages m ON c.id = m.client_id
    GROUP BY c.id
    ORDER BY c.created_at DESC
    ''')
    
    clients = cursor.fetchall()
    conn.close()
    
    if not clients:
        await update.message.reply_text("👥 Нет клиентов.")
        return
    
    text = "👥 <b>Все клиенты:</b>\n\n"
    for client in clients:
        text += f"• ID: {client[0]}\n"
        text += f"  👤 {client[1]}\n"
        text += f"  📋 Задач: {client[3]}\n"
        text += f"  📧 Сообщений: {client[4]}\n\n"
    
    await update.message.reply_text(text, parse_mode='HTML')

# ==================== КЛИЕНТСКИЕ ФУНКЦИИ ==================== #

async def client_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    register_client(user.id, user.first_name, user.last_name, user.username)
    
    text = (
        "👋 <b>Добро пожаловать в наш сервис!</b>\n\n"
        "Я ваш персональный помощник. Здесь вы можете:\n"
        "• 📋 Отслеживать свои задачи\n"
        "• 📦 Проверять статус заказов\n"
        "• 💬 Связаться с поддержкой\n"
        "• 📞 Найти контакты менеджера\n\n"
        "Выберите нужный раздел:"
    )
    await update.message.reply_text(text, reply_markup=client_markup, parse_mode='HTML')

async def show_my_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT id FROM clients WHERE telegram_id = ?
    ''', (update.effective_user.id,))
    
    client = cursor.fetchone()
    if not client:
        await update.message.reply_text("❌ Клиент не найден.")
        return
    
    cursor.execute('''
    SELECT title, description, status, priority 
    FROM tasks 
    WHERE client_id = ? AND status != "завершено"
    ORDER BY created_at DESC
    ''', (client[0],))
    
    tasks = cursor.fetchall()
    conn.close()
    
    if not tasks:
        await update.message.reply_text("📝 У вас нет активных задач.")
        return
    
    text = "📋 <b>Ваши задачи:</b>\n\n"
    for i, task in enumerate(tasks, 1):
        text += f"{i}. <b>{task[0]}</b>\n"
        text += f"   Описание: {task[1]}\n"
        text += f"   Статус: {task[2]} | Приоритет: {task[3]}\n\n"
    
    await update.message.reply_text(text, parse_mode='HTML')

async def show_contacts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "📞 <b>Наши контакты:</b>\n\n"
        "👨‍💼 <b>Ваш персональный менеджер:</b>\n"
        "• Телефон: +7 (999) 123-45-67\n"
        "• Email: manager@yourcompany.com\n"
        "• Telegram: @your_manager\n\n"
        "🛠 <b>Техническая поддержка:</b>\n"
        "• Телефон: +7 (800) 123-45-67\n"
        "• Email: support@yourcompany.com\n"
        "• Рабочее время: Пн-Пт 9:00-18:00\n\n"
        "💼 <b>Бухгалтерия:</b>\n"
        "• Email: accounting@yourcompany.com\n\n"
        "<i>Мы всегда рады вам помочь!</i>"
    )
    await update.message.reply_text(text, parse_mode='HTML')

async def handle_client_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    message_text = update.message.text
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT id FROM clients WHERE telegram_id = ?', (user.id,))
    client = cursor.fetchone()
    
    if client:
        add_message(client[0], message_text, True)
        
        # Уведомление админу
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"📩 <b>Новое сообщение от {user.first_name}:</b>\n\n{message_text}",
            parse_mode='HTML'
        )
    
    conn.close()
    
    await update.message.reply_text(
        "✅ Ваше сообщение отправлено! Мы ответим в ближайшее время.",
        reply_markup=client_markup
    )

# ==================== ОБРАБОТЧИКИ ==================== #

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id == ADMIN_ID:
        await admin_panel(update, context)
    else:
        await client_start(update, context)

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text
    
    if user_id == ADMIN_ID:
        if text == '📊 Все задачи':
            await show_all_tasks(update, context)
        elif text == '👥 Все клиенты':
            await show_all_clients(update, context)
        else:
            await update.message.reply_text("Используйте меню для навигации", reply_markup=admin_markup)
    else:
        if text == '📋 Мои задачи':
            await show_my_tasks(update, context)
        elif text == '📞 Контакты':
            await show_contacts(update, context)
        elif text == '💬 Написать':
            await update.message.reply_text("Напишите ваше сообщение:")
        else:
            await handle_client_message(update, context)

# ==================== ЗАПУСК ==================== #

def main():
    # Инициализация БД
    init_db()
    
    # Создаем тестовые данные
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Добавляем тестовые задачи если их нет
    cursor.execute('SELECT COUNT(*) FROM tasks')
    if cursor.fetchone()[0] == 0:
        cursor.execute('SELECT id FROM clients WHERE telegram_id = ?', (ADMIN_ID,))
        admin_client_id = cursor.fetchone()
        if admin_client_id:
            add_task(admin_client_id[0], "Пример задачи", "Это тестовая задача для демонстрации", "высокий")
    
    conn.close()
    
    # Запуск бота
    application = Application.builder().token(BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    
    print("🚀 Профессиональный клиентский бот запущен!")
    print("📊 База данных инициализирована")
    print(f"👨‍💼 Админ ID: {ADMIN_ID}")
    
    application.run_polling()

if __name__ == '__main__':
    main()
