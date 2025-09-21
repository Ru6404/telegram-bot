import logging
import sqlite3
import os
from dotenv import load_dotenv
from telegram import Bot
from telegram.ext import Updater, CommandHandler

load_dotenv()  # загружаем .env
TOKEN = os.getenv("TELEGRAM_TOKEN")

if not TOKEN:
    raise ValueError("Токен не найден! Проверь .env файл.")

bot = Bot(token=TOKEN)
updater = Updater(token=TOKEN)

def start(update, context):
    update.message.reply_text("Бот работает!")

updater.dispatcher.add_handler(CommandHandler("start", start))

updater.start_polling()
updater.idle()

from datetime import datetime, timedelta
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

# Настройки
BOT_TOKEN = "YOUR_BOT_TOKEN"
ADMIN_ID = 5569793273

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Клавиатура админа
admin_keys = [
    ['📊 Все задачи', '👥 Все клиенты'],
    ['📦 Все заказы', '📨 Рассылка'],
    ['📈 Статистика', '⚙️ Настройки']
]
admin_markup = ReplyKeyboardMarkup(admin_keys, resize_keyboard=True)

# Состояния для ConversationHandler
BROADCAST_MESSAGE = range(1)

# Инициализация базы данных
def init_db():
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()
    
    # Таблица клиентов
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS clients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER UNIQUE,
        username TEXT,
        first_name TEXT,
        last_name TEXT,
        phone TEXT,
        registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        message_count INTEGER DEFAULT 0,
        last_message_date TIMESTAMP
    )
    ''')
    
    # Таблица задач
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_id INTEGER,
        title TEXT,
        description TEXT,
        status TEXT DEFAULT 'active',
        priority TEXT DEFAULT 'medium',
        created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (client_id) REFERENCES clients (id)
    )
    ''')
    
    # Таблица заказов
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_id INTEGER,
        product_name TEXT,
        quantity INTEGER,
        price REAL,
        status TEXT DEFAULT 'new',
        created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (client_id) REFERENCES clients (id)
    )
    ''')
    
    # Таблица сообщений
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_id INTEGER,
        message_text TEXT,
        created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (client_id) REFERENCES clients (id)
    )
    ''')
    
    conn.commit()
    conn.close()

# Добавление тестовых данных
def add_test_data():
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()
    
    # Тестовые клиенты
    test_clients = [
        (1001, 'ivanov', 'Иван', 'Иванов', '+79111111111', 3),
        (1002, 'maria', 'Мария', 'Петрова', '+79222222222', 0),
        (1003, 'alexey', 'Алексей', 'Сидоров', '+79333333333', 0)
    ]
    
    for client in test_clients:
        try:
            cursor.execute('''
            INSERT OR IGNORE INTO clients (user_id, username, first_name, last_name, phone, message_count)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', client)
        except:
            pass
    
    # Тестовые задачи
    tasks = [
        (1001, 'Разработка сайта', 'Создание корпоративного сайта', 'new', 'high'),
        (1001, 'Настройка SEO', 'Оптимизация сайта для поисковых систем', 'new', 'medium'),
        (1001, 'Консультация', 'Консультация по проекту', 'new', 'low')
    ]
    
    for task in tasks:
        cursor.execute('''
        INSERT INTO tasks (client_id, title, description, status, priority)
        VALUES (?, ?, ?, ?, ?)
        ''', task)
    
    conn.commit()
    conn.close()

# Команда start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user = update.effective_user
    
    if user_id == ADMIN_ID:
        # Получаем статистику для админа
        conn = sqlite3.connect('bot_database.db')
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM clients')
        total_clients = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM tasks WHERE status = "active"')
        active_tasks = cursor.fetchone()[0]
        
        # Сообщения за последние 24 часа
        twenty_four_hours_ago = datetime.now() - timedelta(hours=24)
        cursor.execute('SELECT COUNT(*) FROM messages WHERE created_date > ?', (twenty_four_hours_ago,))
        recent_messages = cursor.fetchone()[0]
        
        conn.close()
        
        message = f"""
👨‍💼 <b>Админ-панель</b>

📊 <b>Статистика:</b>
• Клиентов: {total_clients}
• Активных задач: {active_tasks}
• Новых сообщений (24ч): {recent_messages}

Выберите действие:
        """
        
        await update.message.reply_text(message, parse_mode='HTML', reply_markup=admin_markup)
    else:
        await update.message.reply_text("👋 Добро пожаловать! Чем могу помочь?")

# Показать всех клиентов
async def show_all_clients(update: Update, context: ContextTypes.DEFAULT_TYPE):
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT c.id, c.first_name, c.last_name, 
           COUNT(t.id) as task_count, 
           c.message_count
    FROM clients c
    LEFT JOIN tasks t ON c.id = t.client_id AND t.status = "active"
    GROUP BY c.id
    ''')
    
    clients = cursor.fetchall()
    conn.close()
    
    message = "👥 <b>Все клиенты:</b>\n\n"
    
    for client in clients:
        message += f"• ID: {client[0]}\n"
        message += f"  👤 {client[1]} {client[2]}\n"
        message += f"  📋 Задач: {client[3]}\n"
        message += f"  📧 Сообщений: {client[4]}\n\n"
    
    await update.message.reply_text(message, parse_mode='HTML')

# Показать все задачи
async def show_all_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT t.id, t.title, c.first_name, c.last_name, t.status, t.priority
    FROM tasks t
    JOIN clients c ON t.client_id = c.id
    WHERE t.status = "active"
    ORDER BY t.created_date DESC
    ''')
    
    tasks = cursor.fetchall()
    conn.close()
    
    if not tasks:
        await update.message.reply_text("📝 Нет активных задач.")
        return
    
    message = "📊 <b>Все активные задачи:</b>\n\n"
    
    for task in tasks:
        # Эмодзи для приоритета
        priority_emoji = "⚡ высокий" if task[5] == "high" else "🔶 средний" if task[5] == "medium" else "🔻 низкий"
        status_emoji = "🟢 новый" if task[4] == "new" else "🟡 в работе" if task[4] == "in_progress" else "🔴 завершен"
        
        message += f"• #{task[0]}: {task[1]}\n"
        message += f"  👤 {task[2]} {task[3]}\n"
        message += f"  {status_emoji} | {priority_emoji}\n\n"
    
    await update.message.reply_text(message, parse_mode='HTML')

# Показать все заказы
async def show_all_orders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT o.id, c.first_name, c.last_name, o.product_name, o.quantity, o.price, o.status
    FROM orders o
    JOIN clients c ON o.client_id = c.id
    ORDER BY o.created_date DESC
    ''')
    
    orders = cursor.fetchall()
    conn.close()
    
    if not orders:
        message = "📦 <b>Все заказы:</b>\n\nНа данный момент заказов нет."
    else:
        message = "📦 <b>Все заказы:</b>\n\n"
        for order in orders:
            message += f"• Заказ #{order[0]}: {order[3]}\n"
            message += f"  👤 {order[1]} {order[2]}\n"
            message += f"  📦 {order[4]} шт. × {order[5]} руб.\n"
            message += f"  🚦 Статус: {order[6]}\n\n"
    
    await update.message.reply_text(message, parse_mode='HTML')

# Показать статистику
async def show_statistics(update: Update, context: ContextTypes.DEFAULT_TYPE):
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()
    
    # Основная статистика
    cursor.execute('SELECT COUNT(*) FROM clients')
    total_clients = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM tasks WHERE status = "active"')
    active_tasks = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM tasks')
    total_tasks = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM orders')
    total_orders = cursor.fetchone()[0]
    
    cursor.execute('SELECT SUM(price * quantity) FROM orders')
    total_revenue = cursor.fetchone()[0] or 0
    
    # Сообщения за последние 24 часа
    twenty_four_hours_ago = datetime.now() - timedelta(hours=24)
    cursor.execute('SELECT COUNT(*) FROM messages WHERE created_date > ?', (twenty_four_hours_ago,))
    recent_messages = cursor.fetchone()[0]
    
    conn.close()
    
    message = f"""
📈 <b>Статистика:</b>

👥 <b>Клиенты:</b> {total_clients}
📊 <b>Активные задачи:</b> {active_tasks}
📝 <b>Всего задач:</b> {total_tasks}
📦 <b>Заказы:</b> {total_orders}
💰 <b>Выручка:</b> {total_revenue} руб.
📨 <b>Сообщения (24ч):</b> {recent_messages}
    """
    
    await update.message.reply_text(message, parse_mode='HTML')

# Настройки
async def show_settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = """
⚙️ <b>Настройки админ-панели:</b>

• 🔔 Уведомления - настройка оповещений
• 📝 Шаблоны сообщений - редактирование текстов
• 🗄️ Настройки БД - управление базой данных
• 📊 Логирование - настройка логов
• 👥 Права доступа - управление администраторами

Используйте команды для настройки:
/set_notifications - уведомления
/set_templates - шаблоны
/db_backup - backup базы
    """
    
    await update.message.reply_text(message, parse_mode='HTML')

# Начало рассылки
async def start_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📨 Введите сообщение для рассылки:",
        reply_markup=ReplyKeyboardRemove()
    )
    return BROADCAST_MESSAGE

# Отправка рассылки
async def send_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_text = update.message.text
    
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT user_id FROM clients WHERE user_id != ?', (ADMIN_ID,))
    clients = cursor.fetchall()
    conn.close()
    
    total_clients = len(clients)
    successful = 0
    failed = 0
    
    await update.message.reply_text(f"🔄 Начинаю рассылку для {total_clients} клиентов...")
    
    for client in clients:
        try:
            await context.bot.send_message(
                chat_id=client[0],
                text=f"📢 <b>Рассылка от администратора:</b>\n\n{message_text}",
                parse_mode='HTML'
            )
            successful += 1
        except:
            failed += 1
    
    await update.message.reply_text(
        f"✅ Рассылка завершена!\n\n"
        f"✅ Успешно: {successful}\n"
        f"❌ Не удалось: {failed}",
        reply_markup=admin_markup
    )
    
    return ConversationHandler.END

# Отмена рассылки
async def cancel_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "❌ Рассылка отменена.",
        reply_markup=admin_markup
    )
    return ConversationHandler.END

# Обработчик текстовых сообщений
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text
    
    if user_id == ADMIN_ID:
        if text == '📊 Все задачи':
            await show_all_tasks(update, context)
        elif text == '👥 Все клиенты':
            await show_all_clients(update, context)
        elif text == '📦 Все заказы':
            await show_all_orders(update, context)
        elif text == '📨 Рассылка':
            await start_broadcast(update, context)
            return BROADCAST_MESSAGE
        elif text == '📈 Статистика':
            await show_statistics(update, context)
        elif text == '⚙️ Настройки':
            await show_settings(update, context)
        else:
            await update.message.reply_text("Используйте меню для навигации", reply_markup=admin_markup)
    else:
        # Обработка сообщений от клиентов
        conn = sqlite3.connect('bot_database.db')
        cursor = conn.cursor()
        
        # Сохраняем сообщение
        cursor.execute('SELECT id FROM clients WHERE user_id = ?', (user_id,))
        client_result = cursor.fetchone()
        
        if client_result:
            client_id = client_result[0]
            cursor.execute('''
            INSERT INTO messages (client_id, message_text)
            VALUES (?, ?)
            ''', (client_id, text))
            
            # Обновляем счетчик сообщений
            cursor.execute('''
            UPDATE clients 
            SET message_count = message_count + 1, last_message_date = CURRENT_TIMESTAMP
            WHERE id = ?
            ''', (client_id,))
        
        conn.commit()
        conn.close()
        
        await update.message.reply_text("Ваше сообщение получено! Мы свяжемся с вами в ближайшее время.")

# Основная функция
def main():
    # Инициализация базы данных
    init_db()
    add_test_data()
    
    # Создание приложения
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Обработчики команд
    application.add_handler(CommandHandler("start", start))
    
    # ConversationHandler для рассылки
    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Text(['📨 Рассылка']), start_broadcast)],
        states={
            BROADCAST_MESSAGE: [MessageHandler(filters.TEXT & ~filters.Command(), send_broadcast)]
        },
        fallbacks=[CommandHandler("cancel", cancel_broadcast)]
    )
    
    application.add_handler(conv_handler)
    
    # Обработчик текстовых сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.Command(), handle_text))
    
    # Запуск бота
    print("Бот запущен...")
    application.run_polling()

if __name__ == "__main__":
    main()
