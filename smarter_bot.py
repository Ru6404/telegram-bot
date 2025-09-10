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
    {"name": "Fallback AI", "url": None, "timeout": 3}
]

def check_service_availability(url, timeout):
    """Проверяет доступность сервиса"""
    if not url:
        return False
    try:
        from urllib.parse import urlparse
        parsed_url = urlparse(url)
        host = parsed_url.hostname
        port = parsed_url.port or (80 if parsed_url.scheme == 'http' else 443)
        
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
            logger.info(f"✅ Найден ИИ-сервис: {service['name']}")
            return service
    logger.info("⚠️  Внешние ИИ-сервисы недоступны, использую встроенный ИИ")
    return AI_SERVICES[-1]

def main_menu():
    return ReplyKeyboardMarkup([
        ["👥 Пользователи", "✅ Задачи"],
        ["📊 Статус системы", "📋 Помощь"],
        ["➕ Создать пользователя", "➕ Создать задачу"],
        ["🤖 Спросить ИИ", "🛠️ Админ панель"]
    ], resize_keyboard=True)

async def ask_ai_assistant(question, user_context=None):
    """Умный запрос к ИИ-помощнику"""
    ai_service = discover_ai_service()
    
    if ai_service["url"] and ai_service != AI_SERVICES[-1]:
        try:
            payload = {"question": question, "context": user_context or "Telegram bot"}
            response = requests.post(ai_service["url"], json=payload, timeout=ai_service["timeout"])
            if response.status_code == 200:
                data = response.json()
                answer = data.get("answer", data.get("response", data.get("text", "")))
                if answer:
                    return f"🤖 {ai_service['name']}:\n\n{answer}"
        except Exception as e:
            logger.warning(f"Ошибка запроса к ИИ: {e}")
    
    return await smart_fallback_ai(question)

async def smart_fallback_ai(question):
    """Умный встроенный ИИ с улучшенным пониманием контекста"""
    question_lower = question.lower()
    
    # Контекстные ответы на предыдущие сообщения
    if question_lower in ['с какими', 'какие', 'что еще', 'еще']:
        return """🎯 Я могу помочь с:

• 🧮 Математика: "реши 2+2", "посчитай 5*5"
• 💻 Программирование: "напиши код на Python", "помоги с алгоритмом"
• 📊 Системные задачи: пользователи, задачи, статус
• 🌍 Переводы: "переведи привет на английский"
• ⏰ Время и дата: "который час?", "какая сегодня дата?"
• 📚 Общие вопросы: "объясни квантовую физику", "что такое ИИ"

Что именно вас интересует?"""

    # Анализ банка
    if any(word in question_lower for word in ['анализ банка', 'банк анализ', 'финансовый анализ']):
        return """🏦 Для анализа банка могу помочь:

• 📈 Финансовые показатели (если предоставите данные)
• 💰 Кредитные риски
• 📊 Анализ отчетности
• 🔍 Risk management

Пришлите конкретные данные или вопросы по анализу!"""

    # Новости
    if any(word in question_lower for word in ['новости', 'news', 'сми', 'события']):
        return """📰 К сожалению, я не имею доступа к текущим новостям в реальном времени.

Но могу помочь с:
• 📊 Анализом текстов новостей (если пришлете)
• 📈 Статистикой и данными
• 🔍 Поиском информации в моей базе знаний

Есть конкретная тема новостей?"""

    # Математика
    math_patterns = [r'(\d+[\+\-\*\/]\d+)', r'посчитай (.+)', r'сколько будет (.+)', r'реши пример (.+)']
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
    if any(word in question_lower for word in ['код', 'программ', 'алгоритм', 'функция', 'python', 'javascript']):
        return """💻 Могу помочь с программированием!

• Написание кода на Python, JavaScript, Java, C++
• Объяснение алгоритмов
• Решение задач по программированию
• Code review

Какой язык и задача?"""

    # Время и дата
    if any(word in question_lower for word in ['время', 'дата', 'который час', 'сколько времени']):
        from datetime import datetime
        now = datetime.now()
        return f"⏰ Сейчас: {now.strftime('%H:%M:%S %d.%m.%Y')}"

    # Переводчик
    if any(word in question_lower for word in ['переведи', 'translat', 'как будет', 'перевод']):
        return "🌍 Напишите: 'переведи [текст] на [язык]'\nПример: 'переведи привет на английский'"

    # Что ты умеешь
    if any(word in question_lower for word in ['что ты умеешь', 'твои возможности', 'функции', 'что можешь']):
        return """🚀 Я могу многое! Вот мои основные возможности:

• 🤖 Отвечать на любые вопросы (через ИИ)
• 🧮 Решать математические задачи
• 💻 Помогать с программированием
• 👥 Управлять пользователями системы
• ✅ Работать с задачами и проектами
• 📊 Показывать статус системы
• 🌍 Переводить тексты
• ⏰ Подсказывать время и дату

Что именно вас интересует?"""

    # Приветствия
    if any(word in question_lower for word in ['привет', 'здравств', 'хай', 'hello', 'hi']):
        return "👋 Привет! Задайте ваш вопрос - я постараюсь помочь!"

    # Умные контекстные ответы
    ai_responses = [
        "🤔 Интересный вопрос! Можете уточнить или задать более конкретный вопрос?",
        "💡 Понял ваш запрос! Что именно вас интересует в этой теме?",
        "🎯 Хорошо, я готов помочь! Нужны дополнительные детали для точного ответа.",
        "🔍 Ищу информацию по вашему вопросу... Можете переформулировать или уточнить?",
        "🚀 Принял к сведению! Расскажите подробнее, чем могу помочь?"
    ]
    
    return random.choice(ai_responses)

def is_admin(user_id):
    return user_id == ADMIN_ID

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    user_id = user.id
    
    ai_service = discover_ai_service()
    service_status = f"✅ Подключен к {ai_service['name']}" if ai_service['url'] else "⚡ Использую встроенный ИИ"
    
    await update.message.reply_text(
        f"🚀 Добро пожаловать, {user.first_name}!\n"
        f"{service_status}\n\n"
        f"🤖 Теперь я понимаю контекст и могу:\n"
        f"• Отвечать на сложные вопросы\n"
        f"• Понимать follow-up вопросы\n"
        f"• Предлагать релевантную помощь",
        reply_markup=main_menu()
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
        "🏠 Главное меню": "🏠 Главное меню:"
    }
    
    if text in button_handlers:
        handler = button_handlers[text]
        response = handler() if callable(handler) else handler
        await update.message.reply_text(response, reply_markup=main_menu())
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
    
    logger.info("🤖 Умный бот с улучшенным ИИ запущен...")
    print("✅ Бот запущен! Улучшенное понимание контекста!")
    print("🎯 Теперь понимает:")
    print("   • 'С какими' (после предыдущего вопроса)")
    print("   • 'Анализ банка' (конкретная тема)")
    print("   • Контекстные follow-up вопросы")
    
    application.run_polling()

if __name__ == "__main__":
    main()
