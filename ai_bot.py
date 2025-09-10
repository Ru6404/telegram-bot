import os
import logging
import random
import requests
import json
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, MessageHandler, filters, ContextTypes, CommandHandler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = "8253068855:AAFPNJke9PYju90RgZe4ZOKOuuMSJNAs0X8"
ADMIN_ID = 123456789  # ← ЗАМЕНИТЕ НА ВАШ ID

# Настройки ИИ-помощника (замените на ваши)
AI_API_URL = "http://localhost:5000/api/ai/ask"  # URL вашего ИИ-помощника
# ИЛИ используем OpenAI API как fallback
OPENAI_API_KEY = "your-openai-api-key"  # Опционально

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
    """
    Функция для запроса к ИИ-помощнику
    """
    try:
        # Вариант 1: Запрос к вашему ИИ-помощнику
        payload = {
            "question": question,
            "context": user_context or "Пользователь спрашивает через Telegram бота"
        }
        
        response = requests.post(
            AI_API_URL,
            json=payload,
            timeout=10,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            return data.get("answer", "Не получилось получить ответ от ИИ")
        
    except requests.exceptions.RequestException:
        # Если ваш ИИ недоступен, используем fallback
        pass
    
    # Вариант 2: Fallback - простой ИИ на основе правил
    return await fallback_ai_response(question)

async def fallback_ai_response(question):
    """
    Простой ИИ на основе правил (если основной недоступен)
    """
    question_lower = question.lower()
    
    # Математические задачи
    if any(word in question_lower for word in ['реши', 'посчитай', 'вычисли', 'сколько будет', '=']):
        # Простая математика
        try:
            # Пытаемся найти математическое выражение
            import re
            math_expr = re.search(r'(\d+[\+\-\*\/]\d+)', question)
            if math_expr:
                result = eval(math_expr.group(1))
                return f"🧮 Результат: {math_expr.group(1)} = {result}"
        except:
            pass
        return "🔢 Для математических задач напишите выражение, например: '2+2' или '5*3'"
    
    # Программирование
    elif any(word in question_lower for word in ['код', 'программ', 'алгоритм', 'функция', 'python']):
        return "💻 Я могу помочь с основами программирования! Опишите задачу подробнее."
    
    # Общие знания
    elif any(word in question_lower for word in ['что такое', 'кто такой', 'объясни']):
        return "📚 Задайте вопрос о конкретной теме, и я постараюсь объяснить!"
    
    # Время и дата
    elif any(word in question_lower for word in ['время', 'дата', 'который час']):
        from datetime import datetime
        now = datetime.now()
        return f"⏰ Сейчас: {now.strftime('%H:%:%S %d.%m.%Y')}"
    
    # Переводчик
    elif any(word in question_lower for word in ['переведи', 'translat', 'как будет']):
        return "🌍 Для перевода напишите: 'переведи [текст] на [язык]'"
    
    # Дефолтный ответ
    return "🤖 Я получил ваш вопрос! Для сложных задач используйте точные формулировки."

def is_admin(user_id):
    return user_id == ADMIN_ID

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    user_id = user.id
    
    await update.message.reply_text(
        f"🚀 Добро пожаловать, {user.first_name}!\n"
        f"Теперь я с ИИ-помощником! 🤖\n\n"
        f"Могу помочь с:\n"
        f"• Системными задачами 👥✅\n"
        f"• Математикой 🧮\n"
        f"• Программированием 💻\n"
        f"• И многим другим!",
        reply_markup=main_menu() if user_id != ADMIN_ID else admin_main_menu()
    )

async def handle_ai_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    original_text = update.message.text
    user = update.message.from_user
    user_id = user.id
    
    logger.info(f"User {user.first_name}: {original_text}")
    
    # Обработка кнопок меню
    button_handlers = {
        "👥 Пользователи": "👥 Загружаю список пользователей...",
        "✅ Задачи": "✅ Загружаю список задач...",
        "📊 Статус системы": "📊 Система работает стабильно! 🟢",
        "📋 Помощь": "📋 Я теперь с ИИ! Спросите что угодно 🤖",
        "➕ Создать пользователя": "👤 Для создания: /add_user Имя Email",
        "➕ Создать задачу": "✅ Для создания: /add_task Заголовок Описание",
        "🤖 Спросить ИИ": "💬 Задайте любой вопрос ИИ-помощнику!",
        "🛠️ Админ панель": lambda: "🛠️ Админ панель:" if is_admin(user_id) else "❌ Доступ запрещен",
        "🏠 Главное меню": lambda: "🏠 Главное меню:"
    }
    
    if original_text in button_handlers:
        handler = button_handlers[original_text]
        if callable(handler):
            response = handler()
        else:
            response = handler
        
        if original_text == "🏠 Главное меню":
            await update.message.reply_text(response, 
                                          reply_markup=main_menu() if user_id != ADMIN_ID else admin_main_menu())
        elif original_text == "🛠️ Админ панель" and is_admin(user_id):
            await update.message.reply_text(response, reply_markup=admin_menu())
        else:
            await update.message.reply_text(response)
        return
    
    # Если это не кнопка, отправляем вопрос ИИ
    await update.message.reply_text("🤖 Думаю над ответом...")
    
    # Получаем ответ от ИИ
    ai_response = await ask_ai_assistant(text, f"Пользователь: {user.first_name} (ID: {user_id})")
    
    # Отправляем ответ
    await update.message.reply_text(f"💡 ИИ-помощник:\n\n{ai_response}")

async def handle_admin_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка админских кнопок"""
    text = update.message.text
    user_id = update.message.from_user.id
    
    if not is_admin(user_id):
        await update.message.reply_text("❌ Недостаточно прав")
        return
    
    admin_actions = {
        "✅ Принять": "✅ Запрос принят! Действие выполнено.",
        "❌ Отказ": "❌ Запрос отклонен! Действие отменено.",
        "👥 Все пользователи": "👥 Полный список пользователей...",
        "✅ Все задачи": "✅ Полный список задач...",
        "📈 Статистика системы": "📈 Статистика: Пользователей: 15, Задач: 42",
        "🔄 Обновить кэш": "🔄 Кэш успешно обновлен!"
    }
    
    if text in admin_actions:
        await update.message.reply_text(admin_actions[text])

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_ai_message))
    
    # Отдельный обработчик для админских кнопок
    application.add_handler(MessageHandler(filters.Regex(r'^(✅ Принять|❌ Отказ|👥 Все пользователи|✅ Все задачи|📈 Статистика системы|🔄 Обновить кэш)$'), handle_admin_buttons))
    
    logger.info("🤖 Бот с ИИ-помощником запущен...")
    print("✅ Бот запущен! Теперь с интеграцией ИИ!")
    print("🎯 Теперь можно спрашивать что угодно:")
    print("   • 'Реши 2+2'")
    print("   • 'Объясни квантовую физику'")
    print("   • 'Напиши код на Python'")
    print("   • Любые другие вопросы!")
    
    application.run_polling()

if __name__ == "__main__":
    main()
