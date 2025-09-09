import os
import logging
import asyncio
import re
import math
from datetime import datetime, timedelta
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

async def process_message(message: str, user_id: int) -> str:
    """Универсальная обработка входящих сообщений"""
    message_lower = message.lower().strip()
    
    # 0. Команда /start
    if message_lower in ['/start', 'start', 'начать']:
        return "🚀 *Добро пожаловать!* Я ваш универсальный помощник!\n\n" \
               "📋 *Что я умею:*\n" \
               "• 🧮 Решать сложные математические примеры\n" \
               "• 🕐 Показывать время и дату\n" \
               "• 📊 Конвертировать величины\n" \
               "• ❓ Отвечать на вопросы\n" \
               "• 😊 Общаться и поддерживать беседу\n\n" \
               "Просто напишите мне что вам нужно!"
    
    # 1. Математические вычисления
    math_patterns = [
        r'(\d+[\s]*[+\-*/×÷^][\s]*\d+)',
        r'посчитай\s+(.+)',
        r'сколько будет\s+(.+)',
        r'вычисли\s+(.+)',
        r'реши\s+(.+)',
    ]
    
    for pattern in math_patterns:
        match = re.search(pattern, message_lower, re.IGNORECASE)
        if match:
            try:
                if pattern.startswith(r'(\d+'):
                    math_expr = match.group(0)
                else:
                    math_expr = match.group(1)
                
                math_expr = re.sub(r'[^\d+\-*/().^√πe]', '', math_expr)
                math_expr = math_expr.replace('×', '*').replace('÷', '/').replace('^', '**')
                
                safe_chars = set('0123456789+-*/().^√πe ')
                if all(char in safe_chars for char in math_expr):
                    math_expr = math_expr.replace('π', str(math.pi)).replace('e', str(math.e))
                    
                    if '√' in math_expr:
                        math_expr = math_expr.replace('√', 'math.sqrt')
                    
                    result = eval(math_expr, {"__builtins__": None}, {"math": math})
                    return f"🧮 *Результат:* {math_expr} = {result}"
                else:
                    return "❌ *Ошибка:* Недопустимое математическое выражение"
                    
            except ZeroDivisionError:
                return "❌ *Ошибка:* Деление на ноль невозможно"
            except Exception as e:
                return f"❌ *Ошибка вычисления:* {str(e)}"
    
    # 2. Время и дата
    time_patterns = [
        'время', 'который час', 'сколько времени', 'текущее время',
        'дата', 'какое число', 'какой день', 'текущая дата',
        'день недели', 'какой день недели'
    ]
    
    if any(pattern in message_lower for pattern in time_patterns):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        current_date = now.strftime("%d.%m.%Y")
        weekday = now.strftime("%A")
        weekday_ru = {
            'Monday': 'Понедельник', 'Tuesday': 'Вторник', 
            'Wednesday': 'Среда', 'Thursday': 'Четверг',
            'Friday': 'Пятница', 'Saturday': 'Суббота', 
            'Sunday': 'Воскресенье'
        }
        
        return f"📅 *Дата и время:*\n" \
               f"• 🕐 Время: {current_time}\n" \
               f"• 📅 Дата: {current_date}\n" \
               f"• 📆 День недели: {weekday_ru.get(weekday, weekday)}"
    
    # 3. Вопросы о возможностях
    capability_patterns = [
        'что ты умеешь', 'твои возможности', 'команды', 'help', 'помощь',
        'какие задачи', 'что можешь', 'функции', 'умения', 'навыки',
        'что ты можешь', 'твои функции', 'что умеешь', 'расскажи о себе',
        'что ты делаешь', 'чем можешь помочь', 'чем помочь', 'что можно',
        'как пользоваться', 'инструкция', 'руководство', 'справка'
    ]
    
    if any(pattern in message_lower for pattern in capability_patterns):
        return "🤖 *Мои возможности:*\n\n" \
               "• 🧮 *Математика:* Решаю сложные примеры (2+2, 10*5, √9, π*2)\n" \
               "• 🕐 *Время:* Показываю текущее время, дату и день недели\n" \
               "• 📊 *Конвертация:* Помогаю с расчетами\n" \
               "• ❓ *Вопросы:* Отвечаю на различные вопросы\n" \
               "• 😊 *Общение:* Поддерживаю беседу\n\n" \
               "Просто напишите мне что вам нужно!"
    
    # 4. Вопросы о боте
    bot_info_patterns = [
        'кто ты', 'что ты', 'твое имя', 'как тебя зовут', 'ты кто',
        'представься', 'расскажи о себе', 'кто ты такой', 'что за бot',
        'твое имя', 'как зовут'
    ]
    
    if any(pattern in message_lower for pattern in bot_info_patterns):
        return "🤖 *Обо мне:*\n\n" \
               "Я — универсальный бот-помощник! Создан для решения различных задач:\n" \
               "• Математические вычисления\n" \
               "• Ответы на вопросы\n" \
               "• Помощь с информацией\n" \
               "• Поддержка и общение\n\n" \
               "Всегда рад помочь! 😊"
    
    # 5. Приветствия
    greeting_patterns = [
        'привет', 'hello', 'hi', 'здравствуй', 'добрый день', 
        'добрый вечер', 'доброе утро', 'хай', 'салют', 'здаров'
    ]
    
    if any(pattern in message_lower for pattern in greeting_patterns):
        return "👋 *Привет!* Рад вас видеть! Чем могу помочь?"
    
    # 6. Благодарности
    thanks_patterns = [
        'спасибо', 'благодарю', 'thanks', 'thank you', 'мерси',
        'пасиб', 'благодарствую', 'признателен'
    ]
    
    if any(pattern in message_lower for pattern in thanks_patterns):
        return "😊 *Пожалуйста!* Всегда рад помочь!\n" \
               "Если нужна еще помощь — обращайтесь!"
    
    # 7. Прощания
    goodbye_patterns = [
        'пока', 'до свидания', 'goodbye', 'see you', 'до встречи',
        'всего доброго', 'увидимся', 'до завтра', 'спокойной ночи'
    ]
    
    if any(pattern in message_lower for pattern in goodbye_patterns):
        return "👋 *До свидания!* Буду рад помочь снова!\n" \
               "Хорошего дня! 😊"
    
    # 8. Как дела
    if 'как дела' in message_lower or 'как ты' in message_lower:
        return "✨ *Отлично!* Работаю и помогаю пользователям! 😊\n" \
               "А как ваши дела?"
    
    # 9. Что делаешь
    if 'что делаешь' in message_lower or 'чем занят' in message_lower:
        return "💻 *В данный момент:* Помогаю пользователям решать задачи!\n" \
               "Чем могу помочь вам?"
    
    # 10. Анализ и аналитика
    analysis_patterns = [
        'анализ', 'аналитик', 'аналитика', 'проанализируй', 
        'сделай анализ', 'исследование', 'исследуй', 'изучи',
        'разбери', 'проанализировать', 'анализ данных',
        'анализ банка', 'анализ компании', 'анализ рынка',
        'банковский анализ', 'финансовый анализ'
    ]
    
    if any(pattern in message_lower for pattern in analysis_patterns):
        return "📊 *Аналитические возможности:*\n\n" \
               "В настоящее время я могу помочь с:\n" \
               "• 📈 Анализ математических данных\n" \
               "• 🔢 Обработка числовой информации\n" \
               "• 📉 Базовый статистический анализ\n" \
               "• 🧮 Вычислительная аналитика\n\n" \
               "Для сложного анализа банковских данных или бизнес-аналитики " \
               "рекомендую специализированные инструменты. " \
               "Но могу помочь с расчетами и вычислениями! 💡"
    
    # 11. Погода
    if any(word in message_lower for word in ['погода', 'weather', 'температура']):
        return "🌤️ *К сожалению,* функция погоды временно недоступна\n" \
               "Но я могу помочь с другими задачами!"
    
    # 12. Шутки и анекдоты
    joke_patterns = [
        'шутка', 'анекдот', 'расскажи шутку', 'пошути', 'рассмеши',
        'скажи что-нибудь смешное'
    ]
    
    if any(pattern in message_lower for pattern in joke_patterns):
        jokes = [
            "Почему программисты так плохо танцуют? У них нет алгоритма! 💃",
            "Что сказал Java-разработчик, когда упал? - Exception! 😄",
            "Почему математики не любят природу? Там слишком много переменных! 🌿",
            "Как программист называет своего сына? - Сын_1.exe 👶",
            "Почему бот всегда прав? Потому что он работает по алгоритму! 🤖"
        ]
        return f"😄 *Вот шутка:*\n\n{jokes[hash(str(user_id)) % len(jokes)]}"
    
    # 13. Вопросы (заканчиваются на ?)
    if message_lower.endswith('?'):
        question_types = {
            'как': "🤔 *Интересный вопрос!* К сожалению, я не могу дать подробный ответ на этот вопрос",
            'почему': "💡 *Хороший вопрос!* Это требует более глубокого анализа",
            'где': "📍 *Поиск местоположения* временно недоступен",
            'когда': "⏰ *Вопросы о времени* — уточните, пожалуйста",
            'что': "🔍 *Что...* Уточните ваш вопрос, пожалуйста",
            'кто': "👥 *Вопрос о личности* — нужна дополнительная информация"
        }
        
        for key, response in question_types.items():
            if key in message_lower:
                return response
        
        return "❓ *Не совсем понимаю вопрос.* Можете переформулировать?\n" \
               "Попробуйте задать более конкретный вопрос!"
    
    # 14. Короткие сообщения
    if len(message.strip()) < 3:
        return "📝 *Сообщение слишком короткое.* Напишите, пожалуйста, подробнее\n" \
               "Чем могу помочь?"
    
    # 15. Сообщения с числами
    if any(c.isdigit() for c in message):
        return "🔢 *Вижу числа!* Хотите что-то посчитать?\n" \
               "Напишите математический пример: 2+2, 10*5, √9 и т.д."
    
    # 16. Универсальный ответ на ВСЁ остальное
    return "🤖 *Не совсем понял запрос.*\n\n" \
           "📋 *Что я могу:*\n" \
           "• Решить математический пример 🧮\n" \
           "• Показать время и дату 🕐\n" \
           "• Ответить на вопрос ❓\n" \
           "• Помочь с другими задачами 💡\n\n" \
           "Просто напишите, что вам нужно!"

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
        "🚀 *Добро пожаловать!* Я ваш универсальный помощник!\n\n"
        "📋 *Что я умею:*\n"
        "• 🧮 Решать сложные математические примеры\n"
        "• 🕐 Показывать время и дату\n"
        "• 📊 Конвертировать величины\n"
        "• ❓ Отвечаю на вопросы\n"
        "• 😊 Общаться и поддерживать беседу\n\n"
        "Просто напишите мне что вам нужно!",
        parse_mode='Markdown'
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /help"""
    await update.message.reply_text(
        "📋 *Доступные команды:*\n\n"
        "/start - Начать работу с ботом\n"
        "/help - Получить справку\n\n"
        "🤖 *Что я умею:*\n"
        "• Решать математические примеры (2+2, √9, π*2)\n"
        "• Показывать время и дату\n"
        "• Отвечать на вопросы\n"
        "• Поддерживать беседу\n\n"
        "Просто напишите мне что вам нужно!",
        parse_mode='Markdown'
    )

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик ошибок"""
    logger.error(f"Ошибка: {context.error}")

def main():
    """Запуск бота"""
    try:
        application = Application.builder().token(BOT_TOKEN).build()
        
        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        
        application.add_error_handler(error_handler)
        
        logger.info("Бот запущен и готов к работе...")
        print("✅ Бот успешно запущен!")
        print("📱 Теперь можете писать сообщения в Telegram")
        
        application.run_polling()
        
    except Exception as e:
        logger.error(f"Ошибка запуска бота: {e}")
        print(f"❌ Ошибка запуска: {e}")

if __name__ == "__main__":
    main()
