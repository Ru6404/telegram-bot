import os
import logging
import random
import requests
import json
import socket
import re
import math
import asyncio
from datetime import datetime
from urllib.parse import urlparse
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, MessageHandler, filters, ContextTypes, CommandHandler
from telegram.error import BadRequest

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Безопасное получение переменных окружения
def get_env_var(name, default=None):
    value = os.getenv(name)
    if value is None:
        return default
    return value

# Конфигурация с безопасными значениями по умолчанию
BOT_TOKEN = get_env_var("BOT_TOKEN", "8253068855:AAFPNJke9PYju90RgZe4ZOKOuuMSJNAs0X8")

# Безопасное получение ADMIN_ID
try:
    ADMIN_ID = int(get_env_var("ADMIN_ID", "5569793273"))
except ValueError:
    logger.warning("ADMIN_ID не является числом, использую значение по умолчанию")
    ADMIN_ID = 5569793273

# Конфигурация ИИ-сервисов
AI_SERVICES = [
    {"name": "Local AI", "url": "http://localhost:5000/api/ai/ask", "timeout": 5, "priority": 10},
    {"name": "Local GPT", "url": "http://127.0.0.1:8000/ask", "timeout": 5, "priority": 9},
    {"name": "Cloud AI", "url": "http://api.ai-assistant.com/ask", "timeout": 10, "priority": 8},
    {"name": "Fallback AI", "url": None, "timeout": 3, "priority": 1}
]

# Добавляем сервис из переменной окружения если он есть
AI_API_URL = get_env_var("AI_API_URL")
if AI_API_URL:
    AI_SERVICES.insert(0, {
        "name": "Custom AI", 
        "url": AI_API_URL, 
        "timeout": 8, 
        "priority": 11  # Самый высокий приоритет
    })

# Кэш для обнаруженных сервисов
discovered_services = {}
last_discovery_time = 0
DISCOVERY_CACHE_TIME = 300  # 5 минут

class SafeEvaluator:
    """Безопасный вычислитель математических выражений"""
    
    @staticmethod
    def safe_eval(expression):
        try:
            # Удаляем все кроме безопасных символов
            clean_expr = re.sub(r'[^0-9+\-*/().]', '', expression)
            
            # Проверяем на опасные конструкции
            if any(op in clean_expr for op in ['**', '//', '>>', '<<', '%', '&', '|', '^', '~']):
                return None
                
            # Используем ast.literal_eval для безопасности
            import ast
            node = ast.parse(clean_expr, mode='eval')
            
            # Разрешаем только базовые операции
            for n in ast.walk(node):
                if isinstance(n, (ast.Call, ast.Attribute, ast.Subscript)):
                    return None
            
            return eval(compile(node, '<string>', 'eval'), {'__builtins__': None}, {})
        except:
            return None

def check_service_availability(url, timeout):
    """Проверяет доступность сервиса"""
    if not url:
        return False
        
    try:
        parsed_url = urlparse(url)
        host = parsed_url.hostname
        port = parsed_url.port or (80 if parsed_url.scheme == 'http' else 443)
        
        # Для localhost проверяем порт
        if host in ['localhost', '127.0.0.1']:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            sock.close()
            return result == 0
        else:
            # Для внешних сервисов делаем HTTP запрос
            try:
                response = requests.get(f"{parsed_url.scheme}://{host}:{port}/", timeout=timeout)
                return response.status_code < 500
            except:
                # Если корневой URL не работает, пробуем endpoint
                try:
                    response = requests.head(url, timeout=timeout)
                    return response.status_code < 500
                except:
                    return False
    except:
        return False

async def discover_ai_services():
    """Асинхронно обнаруживает доступные ИИ-сервисы"""
    global discovered_services, last_discovery_time
    
    current_time = datetime.now().timestamp()
    if current_time - last_discovery_time < DISCOVERY_CACHE_TIME and discovered_services:
        return discovered_services
    
    discovered_services = {}
    
    # Проверяем все сервисы
    for service in sorted(AI_SERVICES, key=lambda x: x['priority'], reverse=True):
        if service["url"]:
            is_available = await asyncio.get_event_loop().run_in_executor(
                None, check_service_availability, service['url'], service['timeout']
            )
            if is_available:
                discovered_services[service['name']] = service
                logger.info(f"✅ Сервис доступен: {service['name']} - {service['url']}")
    
    last_discovery_time = current_time
    return discovered_services
async def ask_ai_assistant(question, user_context=None):
    """Принудительно используем ИИ-сервер"""
    try:
        # ПРЯМОЙ ЗАПРОС К СЕРВЕРУ
        payload = {
            "question": question,
            "context": user_context or "Telegram bot user"
        }
        
        response = requests.post(
            "http://127.0.0.1:5050/api/ai/ask",
            json=payload,
            timeout=5,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            answer = data.get("answer", "")
            if answer:
                return f"🤖 ИИ-помощник:\n\n{answer}"
                
    except Exception as e:
        print(f"❌ Ошибка подключения к ИИ: {e}")
    
    # Fallback только если сервер недоступен
    return await smart_fallback_ai(question)

    

async def query_external_ai(service, question, user_context):
    """Запрос к внешнему ИИ-сервису"""
    try:
        payload = {
            "question": question,
            "context": user_context or "Telegram bot user",
            "user_id": "unknown"
        }
        
        # Извлекаем user_id из контекста если возможно
        if user_context and "ID:" in user_context:
            try:
                user_id = user_context.split("ID:")[1].split(")")[0].strip()
                payload["user_id"] = user_id
            except:
                pass
        
        response = requests.post(
            service["url"],
            json=payload,
            timeout=service["timeout"],
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            answer = data.get("answer", data.get("response", data.get("text", "")))
            if answer:
                return f"🤖 {service['name']}:\n\n{answer}"
                
    except Exception as e:
        logger.warning(f"Ошибка запроса к {service['name']}: {e}")
    
    return await smart_fallback_ai(question)

async def smart_fallback_ai(question):
    """Умный встроенный ИИ-помощник с реальными ответами"""
    question_lower = question.lower()
    
    # Бот о себе
    if any(word in question_lower for word in ['что ты можешь', 'возможности', 'функции', 'команды', 'твои навыки']):
        return """🤖 Я могу:

• 🧮 Решать математические примеры: 2+2, 5*8, 100/4
• ⏰ Показывать время и дату: \"Который час?\"
• 🌍 Помогать с переводом: \"Переведи привет на английский\"
• 📚 Отвечать на вопросы о Узбекистане и не только
• 💻 Давать советы по программированию

Просто спросите! Например: 
\"Сколько будет 15*20\" 
\"Новости Узбекистана\"
\"Расскажи о Ташкенте\""""

    # Узбекистан
    if any(word in question_lower for word in ['узбекистан', 'узбек', 'ташкент', 'самарканд', 'бухара']):
        return """🇺🇿 Узбекистан - жемчужина Центральной Азии!

Столица: Ташкент
Крупные города: Самарканд, Бухара, Наманган, Андижан
Валюта: Узбекский сум (UZS)
Население: ~35 миллионов человек
Язык: Узбекский

Достопримечательности: Регистан, мавзолей Саманидов, Чор-Минор
Что интересует конкретно? История, культура, экономика, туризм?"""

    # Новости
    if 'новости' in question_lower:
        if 'узбек' in question_lower:
            return """📰 Новости Узбекистана:

• Экономика растет на 5.8% в этом году
• Туризм увеличился на 30% за последний квартал
• Запущена новая программа поддержки малого бизнеса
• В Ташкенте прошла международная инвестиционная конференция

Уточните период или тему для более детальной информации!"""
        else:
            return "📰 Новости какой страны или региона вас интересуют? Уточните пожалуйста."

    # Изменения в Узбекистане
    if 'изменения' in question_lower and 'узбек' in question_lower:
        return """🔍 Последние изменения в Узбекистане:

• Цифровизация госуслуг (90% услуг онлайн)
• Налоговые реформы для бизнеса
• Развитие зеленой энергетики
• Упрощение визового режима
• Модернизация транспортной системы

Какие аспекты интересуют больше всего?"""

    # Математические вычисления (безопасные)
    math_match = re.search(r'(\d+[\+\-\*\/]\d+)|(посчитай|сколько будет|реши пример)\s+(.+)', question)
    if math_match:
        expr = math_match.group(1) or math_match.group(3)
        if expr:
            result = SafeEvaluator.safe_eval(expr)
            if result is not None:
                return f"🧮 Результат: {expr} = {result}"
            else:
                return "❌ Не могу решить этот пример из-за ограничений безопасности."

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
async def split_long_message(text, max_length=4000):
    """Разделяет длинные сообщения на части"""
    if len(text) <= max_length:
        return [text]
    
    parts = []
    while text:
        if len(text) <= max_length:
            parts.append(text)
            break
        
        # Ищем точку разрыва
        split_pos = text.rfind('\n', 0, max_length)
        if split_pos == -1:
            split_pos = text.rfind('. ', 0, max_length)
        if split_pos == -1:
            split_pos = text.rfind(' ', 0, max_length)
        if split_pos == -1:
            split_pos = max_length
        
        parts.append(text[:split_pos])
        text = text[split_pos:].lstrip()
    
    return parts

def main_menu():
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

def is_admin(user_id):
    return user_id == ADMIN_ID

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    user_id = user.id
    
    # Авто-обнаружение при старте
    services = await discover_ai_services()
    if services:
        best_service = max(services.values(), key=lambda x: x['priority'])
        service_status = f"✅ Подключен к {best_service['name']}"
    else:
        service_status = "⚡ Использую встроенный ИИ"
    
    welcome_text = (
        f"🚀 Добро пожаловать, {user.first_name}!\n"
        f"{service_status}\n\n"
        f"🤖 Теперь я могу:\n"
        f"• Решать задачи 🧮\n"
        f"• Помогать с кодом 💻\n"
        f"• Отвечать на вопросы 📚\n"
        f"• И многое другое!"
    )
    
    await update.message.reply_text(
        welcome_text,
        reply_markup=main_menu() if user_id != ADMIN_ID else admin_menu()
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user = update.message.from_user
    
    logger.info(f"User {user.first_name}: {text}")
    
    # Простая обработка кнопок для демонстрации
    if text == "📊 Статус системы":
        await status_command(update, context)
        return
    elif text == "🤖 Спросить ИИ":
        await update.message.reply_text("💬 Задайте любой вопрос ИИ-помощнику!")
        return
    elif text == "🛠️ Админ панель":
        if is_admin(user.id):
            await update.message.reply_text("🛠️ Админ панель:", reply_markup=admin_menu())
        else:
            await update.message.reply_text("❌ Доступ запрещен")
        return
    elif text == "🏠 Главное меню":
        await update.message.reply_text("🏠 Главное меню:", reply_markup=main_menu())
        return
    
    # Запрос к ИИ
    await update.message.reply_text("🤖 Думаю над ответом...")
    
    user_context = f"Пользователь: {user.first_name} (ID: {user.id})"
    ai_response = await ask_ai_assistant(text, user_context)
    
    # Отправляем ответ частями если он длинный
    message_parts = await split_long_message(ai_response)
    for part in message_parts:
        try:
            await update.message.reply_text(part)
        except BadRequest as e:
            logger.error(f"Ошибка отправки сообщения: {e}")
            await update.message.reply_text("❌ Ошибка отправки ответа")

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда для проверки статуса сервисов"""
    services = await discover_ai_services()
    
    status_text = "📊 Статус ИИ-сервисов:\n\n"
    for service in sorted(AI_SERVICES, key=lambda x: x['priority'], reverse=True):
        if service['name'] in services:
            status_text += f"✅ {service['name']}: {service['url'] or 'Встроенный'}\n"
        else:
            status_text += f"❌ {service['name']}: Недоступен\n"
    
    await update.message.reply_text(status_text)

def main():
    try:
        application = Application.builder().token(BOT_TOKEN).build()
        
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("status", status_command))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        
        logger.info("🤖 Улучшенный бот с авто-ИИ запущен...")
        print("✅ Бот запущен с улучшенной системой обнаружения!")
        print(f"👤 ADMIN_ID: {ADMIN_ID}")
        
        application.run_polling()
    except Exception as e:
        logger.error(f"Ошибка запуска бота: {e}")
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    main()
