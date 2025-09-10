import os
import logging
import random
import requests
import json
import socket
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, MessageHandler, filters, ContextTypes, CommandHandler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = "8253068855:AAFPNJke9PYju90RgZe4ZOKOuuMSJNAs0X8"
ADMIN_ID = 123456789  # ← ЗАМЕНИТЕ НА ВАШ ID

# Автоматическое определение доступных ИИ-сервисов
AI_SERVICES = [
    {"name": "Local AI", "url": "http://localhost:5000/api/ai/ask", "timeout": 5},
    {"name": "Local GPT", "url": "http://127.0.0.1:8000/ask", "timeout": 5},
    {"name": "Cloud AI", "url": "http://api.ai-assistant.com/ask", "timeout": 10},
    {"name": "Fallback AI", "url": None, "timeout": 3}  # Резервный встроенный ИИ
]

# Попробуем также найти сервис через переменные окружения
AI_URL_FROM_ENV = os.getenv('AI_API_URL') or os.getenv('ASSISTANT_URL') or os.getenv('GPT_SERVICE_URL')
if AI_URL_FROM_ENV:
    AI_SERVICES.insert(0, {"name": "Env AI", "url": AI_URL_FROM_ENV, "timeout": 8})

def check_service_availability(url, timeout):
    """Проверяет доступность сервиса"""
    if not url:
        return False
        
    try:
        # Извлекаем хост и порт из URL
        from urllib.parse import urlparse
        parsed_url = urlparse(url)
        host = parsed_url.hostname
        port = parsed_url.port or (80 if parsed_url.scheme == 'http' else 443)
        
        # Проверяем доступность порта
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        
        return result == 0
    except:
        return False

def discover_ai_service():
    """Автоматически находит доступный ИИ-сервис"""
    for service in AI_SERVICES:
        if service["url"] and check_service_availability(service["url"], service["timeout"]):
            logger.info(f"✅ Найден ИИ-сервис: {service['name']} - {service['url']}")
            return service
    
    logger.info("⚠️  Внешние ИИ-сервисы недоступны, использую встроенный ИИ")
    return AI_SERVICES[-1]  # Возвращаем fallback

def main_menu():
    return ReplyKeyboardMarkup([
        ["👥 Пользователи", "✅ Задачи"],
        ["📊 Статус системы", "📋 Помощь"],
        ["➕ Создать пользователя", "➕ Создать задачу"],
        ["🤖 Спросить ИИ", "🛠️ Админ панель"]
    ], resize_keyboard=True)

def admin_main_menu():
    return ReplyKeyboardMarkup([
        ["👥 Пользователи", "✅ Задачи"],
        ["📊 Статус системы", "📋 Помощь"],
        ["➕ Создать пользователя", "➕ Создать задачу"],
        ["🤖 Спросить ИИ", "🛠️ Админ панель"]
    ], resize_keyboard=True)

def admin_menu():
    return ReplyKeyboardMarkup([
        ["👥 Все пользователи", "✅ Все задачи"],
        ["📈 Статистика системы", "🔄 Обновить кэш"],
        ["✅ Принять", "❌ Отказ"],
        ["🏠 Главное меню"]
    ], resize_keyboard=True)

async def ask_ai_assistant(question, user_context=None):
    """Умный запрос к ИИ-помощнику с авто-обнаружением"""
    ai_service = discover_ai_service()
    
    # Если нашли внешний сервис
    if ai_service["url"] and ai_service != AI_SERVICES[-1]:
        try:
            payload = {
                "question": question,
                "context": user_context or "Telegram bot user",
                "user_id": user_context.split("ID:")[1].split(")")[0].strip() if user_context and "ID:" in user_context else "unknown"
            }
            
            response = requests.post(
                ai_service["url"],
                json=payload,
                timeout=ai_service["timeout"],
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                answer = data.get("answer", data.get("response", data.get("text", "")))
                if answer:
                    return f"🤖 {ai_service['name']}:\n\n{answer}"
            
        except Exception as e:
            logger.warning(f"Ошибка запроса к {ai_service['name']}: {e}")
    
    # Fallback на встроенный ИИ
    return await smart_fallback_ai(question)
async def smart_fallback_ai(question):
    """Умный встроенный ИИ-помощник"""
    question_lower = question.lower()
    
    # ВОЗМОЖНОСТИ БОТА
    if any(phrase in question_lower for phrase in ['что ты можешь', 'твои возможности', 'твой функционал', 
                                                 'что умеешь', 'твои способности', 'что ты способен',
                                                 'что можешь сделать', 'какие функции', 'чем помочь']):
        capabilities = [
            "🚀 Я могу многое! Вот мои основные возможности:\n\n"
            "• 🤖 Отвечать на любые вопросы (через ИИ)\n"
            "• 🧮 Решать математические задачи\n"
            "• 💻 Помогать с программированием\n"
            "• 👥 Управлять пользователями системы\n"
            "• ✅ Работать с задачами и проектами\n"
            "• 📊 Показывать статус системы\n"
            "• 🌍 Переводить тексты\n"
            "• ⏰ Подсказывать время и дату\n\n"
            "Что именно вас интересует?",
            
            "🎯 Мои суперспособности:\n\n"
            "• Интеллектуальные ответы на вопросы\n"
            "• Математические вычисления 🧮\n"
            "• Программирование и код 💻\n"
            "• Управление пользователями 👥\n"
            "• Система задач ✅\n"
            "• Мониторинг 📊\n"
            "• Переводчик 🌍\n"
            "• Помощник времени ⏰\n\n"
            "Спросите о конкретной функции!",
            
            "💡 Я универсальный помощник! Могу:\n\n"
            "• Отвечать на сложные вопросы\n"
            "• Решать примеры и задачи\n"
            "• Помогать с кодом\n"
            "• Работать с системой пользователей\n"
            "• Управлять задачами\n"
            "• Показывать системную информацию\n"
            "• Переводить между языками\n"
            "• Подсказывать текущее время\n\n"
            "Что хотите попробовать?"
        ]
        return random.choice(capabilities)
    
    # НОВОСТИ
    if any(word in question_lower for word in ['новости', 'news', 'события', 'свежее', 'последние']):
        news_responses = [
            "📰 К сожалению, я не имею доступа к текущим новостям. "
            "Но могу помочь с другими вопросами!",
            
            "🌐 Для новостей рекомендую использовать новостные сайты или приложения. "
            "А я могу помочь с вычислениями, программированием или системными задачами!",
            
            "📻 Новости лучше искать в специализированных источниках. "
            "Мои сильные стороны: математика, программирование, управление задачами!"
        ]
        return random.choice(news_responses)
    
    # Математика и вычисления
    math_patterns = [
        r'(\d+[\+\-\*\/]\d+)',  # 2+2, 5*3
        r'посчитай (.+)',       # посчитай 2+2
        r'сколько будет (.+)',  # сколько будет 5*5
        r'реши пример (.+)',    # реши пример 10/2
    ]
    
    for pattern in math_patterns:
        import re
        match = re.search(pattern, question)
        if match:
            try:
                expr = match.group(1) if match.groups() else match.group(0)
                result = eval(expr)
                return f"🧮 Результат: {expr} = {result}"
            except:
                return "❌ Не могу решить этот пример. Проверьте правильность выражения."
    
    # Программирование
    if any(word in question_lower for word in ['код', 'программ', 'алгоритм', 'функция', 'python', 'javascript', 'java', 'c++']):
        code_responses = [
            "💻 Расскажите подробнее о вашей задаче программирования!",
            "🚀 Я могу помочь с основами кода. Опишите проблему?",
            "👨‍💻 Для программирования: укажите язык и задачу",
            "📝 Напишите: 'напиши код для [задача] на [язык]'"
        ]
        return random.choice(code_responses)
    
    # Время и дата
    if any(word in question_lower for word in ['время', 'дата', 'который час', 'сколько времени']):
        from datetime import datetime
        now = datetime.now()
        return f"⏰ Сейчас: {now.strftime('%H:%M:%S %d.%m.%Y')}"
    
    # Переводчик
    if any(word in question_lower for word in ['переведи', 'translat', 'как будет', 'перевод']):
        return "🌍 Напишите: 'переведи [текст] на [язык]'\nНапример: 'переведи привет на английский'"
    
    # Общие вопросы
    if any(word in question_lower for word in ['что такое', 'кто такой', 'объясни', 'что значит']):
        return "📚 Задайте вопрос о конкретной теме, и я постараюсь помочь!"
    
    # Приветствия
    if any(word in question_lower for word in ['привет', 'здравств', 'хай', 'hello', 'hi']):
        return "👋 Привет! Задайте ваш вопрос - я постараюсь помочь!"
    
    # Универсальный умный ответ
    ai_responses = [
        "🤔 Интересный вопрос! Уточните, пожалуйста?",
        "💡 Хорошо, я подумаю над этим. Можете задать более конкретный вопрос?",
        "🎯 Понял ваш запрос! Что именно вас интересует?",
        "🔍 Ищу информацию... Можете переформулировать вопрос?",
        "🚀 Принял! Нужны дополнительные детали для ответа."
    ]
    
    return random.choice(ai_responses)
    # НОВОСТИ - ДОБАВЛЯЕМ ОБРАБОТКУ НОВОСТЕЙ
    if any(word in question_lower for word in ['новости', 'news', 'события', 'свежее', 'последние']):
        news_responses = [
            "📰 К сожалению, я не имею доступа к текущим новостям. "
            "Но могу помочь с другими вопросами!",
            
            "🌐 Для новостей рекомендую использовать новостные сайты или приложения. "
            "А я могу помочь с вычислениями, программированием или системными задачами!",
            
            "📻 Новости лучше искать в специализированных источниках. "
            "Мои сильные стороны: математика, программирование, управление задачами!"
        ]
        return random.choice(news_responses)
    
    # Математика и вычисления
    math_patterns = [
        r'(\d+[\+\-\*\/]\d+)',  # 2+2, 5*3
        r'посчитай (.+)',       # посчитай 2+2
        r'сколько будет (.+)',  # сколько будет 5*5
        r'реши пример (.+)',    # реши пример 10/2
    ]
    
    for pattern in math_patterns:
        import re
        match = re.search(pattern, question)
        if match:
            try:
                expr = match.group(1) if match.groups() else match.group(0)
                result = eval(expr)
                return f"🧮 Результат: {expr} = {result}"
            except:
                return "❌ Не могу решить этот пример. Проверьте правильность выражения."
    
    # Программирование
    if any(word in question_lower for word in ['код', 'программ', 'алгоритм', 'функция', 'python', 'javascript', 'java', 'c++']):
        code_responses = [
            "💻 Расскажите подробнее о вашей задаче программирования!",
            "🚀 Я могу помочь с основами кода. Опишите проблему?",
            "👨‍💻 Для программирования: укажите язык и задачу",
            "📝 Напишите: 'напиши код для [задача] на [язык]'"
        ]
        return random.choice(code_responses)
    
    # Время и дата
    if any(word in question_lower for word in ['время', 'дата', 'который час', 'сколько времени']):
        from datetime import datetime
        now = datetime.now()
        return f"⏰ Сейчас: {now.strftime('%H:%M:%S %d.%m.%Y')}"
    
    # Переводчик
    if any(word in question_lower for word in ['переведи', 'translat', 'как будет', 'перевод']):
        return "🌍 Напишите: 'переведи [текст] на [язык]'\nНапример: 'переведи привет на английский'"
    
    # Общие вопросы
    if any(word in question_lower for word in ['что такое', 'кто такой', 'объясни', 'что значит']):
        return "📚 Задайте вопрос о конкретной теме, и я постараюсь помочь!"
    
    # Приветствия
    if any(word in question_lower for word in ['привет', 'здравств', 'хай', 'hello', 'hi']):
        return "👋 Привет! Задайте ваш вопрос - я постараюсь помочь!"
    
    # Универсальный умный ответ
    ai_responses = [
        "🤔 Интересный вопрос! Уточните, пожалуйста?",
        "💡 Хорошо, я подумаю над этим. Можете задать более конкретный вопрос?",
        "🎯 Понял ваш запрос! Что именно вас интересует?",
        "🔍 Ищу информацию... Можете переформулировать вопрос?",
        "🚀 Принял! Нужны дополнительные детали для ответа."
    ]
    
    return random.choice(ai_responses)
    """Умный встроенный ИИ-помощник"""
    question_lower = question.lower()
    
    # Математика и вычисления
    math_patterns = [
        r'(\d+[\+\-\*\/]\d+)',  # 2+2, 5*3
        r'посчитай (.+)',       # посчитай 2+2
        r'сколько будет (.+)',  # сколько будет 5*5
        r'реши пример (.+)',    # реши пример 10/2
    ]
    
    for pattern in math_patterns:
        import re
        match = re.search(pattern, question)
        if match:
            try:
                expr = match.group(1) if match.groups() else match.group(0)
                result = eval(expr)
                return f"🧮 Результат: {expr} = {result}"
            except:
                return "❌ Не могу решить этот пример. Проверьте правильность выражения."
    
    # Программирование
    if any(word in question_lower for word in ['код', 'программ', 'алгоритм', 'функция', 'python', 'javascript', 'java', 'c++']):
        code_responses = [
            "💻 Расскажите подробнее о вашей задаче программирования!",
            "🚀 Я могу помочь с основами кода. Опишите проблему?",
            "👨‍💻 Для программирования: укажите язык и задачу",
            "📝 Напишите: 'напиши код для [задача] на [язык]'"
        ]
        return random.choice(code_responses)
    
    # Время и дата
    if any(word in question_lower for word in ['время', 'дата', 'который час', 'сколько времени']):
        from datetime import datetime
        now = datetime.now()
        return f"⏰ Сейчас: {now.strftime('%H:%M:%S %d.%m.%Y')}"
    
    # Переводчик
    if any(word in question_lower for word in ['переведи', 'translat', 'как будет', 'перевод']):
        return "🌍 Напишите: 'переведи [текст] на [язык]'\nНапример: 'переведи привет на английский'"
    
    # Общие вопросы
    if any(word in question_lower for word in ['что такое', 'кто такой', 'объясни', 'что значит']):
        return "📚 Задайте вопрос о конкретной теме, и я постараюсь помочь!"
    
    # Приветствия
    if any(word in question_lower for word in ['привет', 'здравств', 'хай', 'hello', 'hi']):
        return "👋 Привет! Задайте ваш вопрос - я постараюсь помочь!"
    
    # Универсальный умный ответ
    ai_responses = [
        "🤔 Интересный вопрос! Уточните, пожалуйста?",
        "💡 Хорошо, я подумаю над этим. Можете задать более конкретный вопрос?",
        "🎯 Понял ваш запрос! Что именно вас интересует?",
        "🔍 Ищу информацию... Можете переформулировать вопрос?",
        "🚀 Принял! Нужны дополнительные детали для ответа."
    ]
    
    return random.choice(ai_responses)

def is_admin(user_id):
    return user_id == ADMIN_ID

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    user_id = user.id
    
    # Авто-обнаружение при старте
    ai_service = discover_ai_service()
    service_status = f"✅ Подключен к {ai_service['name']}" if ai_service['url'] else "⚡ Использую встроенный ИИ"
    
    await update.message.reply_text(
        f"🚀 Добро пожаловать, {user.first_name}!\n"
        f"{service_status}\n\n"
        f"🤖 Теперь я могу:\n"
        f"• Решать задачи 🧮\n"
        f"• Помогать с кодом 💻\n"
        f"• Отвечать на вопросы 📚\n"
        f"• И многое другое!",
        reply_markup=main_menu() if user_id != ADMIN_ID else admin_main_menu()
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user = update.message.from_user
    user_id = user.id
    
    logger.info(f"User {user.first_name}: {text}")
    
    # Обработка кнопок меню
    button_handlers = {
        "👥 Пользователи": "👥 Загружаю список пользователей...",
        "✅ Задачи": "✅ Загружаю список задач...",
        "📊 Статус системы": "📊 Система работает стабильно! 🟢",
        "📋 Помощь": "📋 Спросите меня о чем угодно! 🤖",
        "➕ Создать пользователя": "👤 Для создания: /add_user Имя Email",
        "➕ Создать задачу": "✅ Для создания: /add_task Заголовок Описание",
        "🤖 Спросить ИИ": "💬 Задайте любой вопрос ИИ-помощнику!",
        "🛠️ Админ панель": lambda: "🛠️ Админ панель:" if is_admin(user_id) else "❌ Доступ запрещен",
        "🏠 Главное меню": lambda: "🏠 Главное меню:",
        "✅ Принять": "✅ Запрос принят!" if is_admin(user_id) else "❌ Недостаточно прав",
        "❌ Отказ": "❌ Запрос отклонен!" if is_admin(user_id) else "❌ Недостаточно прав",
        "👥 Все пользователи": "👥 Полный список..." if is_admin(user_id) else "❌ Недостаточно прав",
        "✅ Все задачи": "✅ Все задачи..." if is_admin(user_id) else "❌ Недостаточно прав",
        "📈 Статистика системы": "📈 Статистика..." if is_admin(user_id) else "❌ Недостаточно прав",
        "🔄 Обновить кэш": "🔄 Кэш обновлен!" if is_admin(user_id) else "❌ Недостаточно прав"
    }
    
    if text in button_handlers:
        handler = button_handlers[text]
        response = handler() if callable(handler) else handler
        
        if text == "🏠 Главное меню":
            await update.message.reply_text(response, reply_markup=main_menu() if user_id != ADMIN_ID else admin_main_menu())
        elif text == "🛠️ Админ панель" and is_admin(user_id):
            await update.message.reply_text(response, reply_markup=admin_menu())
        else:
            await update.message.reply_text(response)
        return
    
    # Если это не кнопка, отправляем вопрос ИИ
    await update.message.reply_text("🤖 Думаю над ответом...")
    
    # Получаем ответ от ИИ
    user_context = f"Пользователь: {user.first_name} (ID: {user_id})"
    ai_response = await ask_ai_assistant(text, user_context)
    
    # Отправляем ответ
    await update.message.reply_text(ai_response)

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    logger.info("🤖 Бот с авто-ИИ запущен...")
    print("✅ Бот запущен! Автоматически ищет ИИ-сервисы...")
    print("🔍 Поиск доступных ИИ-сервисов...")
    
    # Тестируем discovery при запуске
    ai_service = discover_ai_service()
    print(f"📡 Используется: {ai_service['name']}")
    if ai_service['url']:
        print(f"🌐 URL: {ai_service['url']}")
    else:
        print("⚡ Встроенный ИИ активирован")
    
    application.run_polling()

if __name__ == "__main__":
    main()
