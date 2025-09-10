import os
import random
import re
from datetime import datetime
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# КОНФИГУРАЦИЯ - ЗАМЕНИТЕ ID НА СВОЙ!
BOT_TOKEN = "8253068855:AAFPNJke9PYju90RgZe4ZOKOuuMSJNAs0X8"
ADMIN_ID = 5569793273

def is_admin(user_id):
    return user_id == ADMIN_ID

def calculate_math(expression):
    """Безопасные математические вычисления"""
    try:
        # Разрешаем только цифры и основные операторы
        if not re.match(r'^[\d\s\+\-\*\/\(\)\.]+$', expression):
            return None
        
        # Запрещаем опасные операции
        if any(op in expression for op in ['**', '//', '%', '&', '|', '^', '~', '=']):
            return None
            
        result = eval(expression, {"__builtins__": None}, {})
        return result
    except:
        return None

def generate_response(message):
    """Генератор умных ответов"""
    message_lower = message.lower()
    
    # Приветствие
    if any(word in message_lower for word in ['привет', 'здравств', 'hello', 'hi']):
        return "👋 Привет! Я бот-помощник. Спросите меня о чем угодно!"
    
    # Бот о себе
    if any(word in message_lower for word in ['что ты можешь', 'возможности', 'функции']):
        return """🤖 Я могу:
• 🧮 Решать примеры: 2+2, 5*8, 100/4
• ⏰ Показывать время и дату
• 🇺🇿 Рассказывать об Узбекистане
• 🌍 Помогать с переводом
• 💻 Давать советы по программированию

Спросите: \"Новости Узбекистана\" или \"Сколько будет 15*20\""""

    # Узбекистан
    if any(word in message_lower for word in ['узбекистан', 'узбек', 'ташкент', 'самарканд', 'бухара']):
        return """🇺🇿 Узбекистан - жемчужина Центральной Азии!

Столица: Ташкент
Население: ~35 миллионов человек
Валюта: Узбекский сум
Язык: Узбекский

Достопримечательности: Регистан, мавзолей Саманидов, Чор-Минор
Что интересует конкретно? История, культура, экономика, туризм?"""

    # Новости
    if 'новости' in message_lower:
        if 'узбек' in message_lower:
            return """📰 Новости Узбекистана:

• Экономика растет на 5.8% в этом году
• Туризм увеличился на 30% за последний квартал
• Запущена новая программа поддержки малого бизнеса
• В Ташкенте прошла международная инвестиционная конференция

Уточните период или тему для более детальной информации!"""
        else:
            return "📰 Новости какой страны или региона вас интересуют? Уточните пожалуйста."

    # Изменения в Узбекистане
    if 'изменения' in message_lower and 'узбек' in message_lower:
        return """🔍 Последние изменения в Узбекистане:

• Цифровизация госуслуг (90% услуг онлайн)
• Налоговые реформы для бизнеса
• Развитие зеленой энергетики
• Упрощение визового режима
• Модернизация транспортной системы

Какие аспекты интересуют больше всего?"""

    # Математика
    math_match = re.search(r'(\d+[\+\-\*\/]\d+)|(посчитай|сколько будет|реши пример)\s+(.+)', message)
    if math_match:
        expr = math_match.group(1) or math_match.group(3)
        if expr:
            result = calculate_math(expr)
            if result is not None:
                return f"🧮 Результат: {expr} = {result}"
            else:
                return "❌ Не могу решить этот пример."

    # Время
    if any(word in message_lower for word in ['время', 'дата', 'который час', 'сколько времени']):
        return f"⏰ Сейчас: {datetime.now().strftime('%H:%M:%S %d.%m.%Y')}"

    # Переводчик
    if any(word in message_lower for word in ['переведи', 'translat', 'как будет', 'перевод']):
        return "🌍 Напишите: 'переведи [текст] на [язык]'\nНапример: 'переведи привет на английский'"

    # Общие вопросы
    if any(word in message_lower for word in ['что такое', 'кто такой', 'объясни', 'что значит']):
        return "📚 Задайте вопрос о конкретной теме, и я постараюсь помочь!"

    # Универсальный умный ответ
    responses = [
        "🤔 Интересный вопрос! Уточните, пожалуйста?",
        "💡 Хорошо, я подумаю над этим. Можете задать более конкретный вопрос?",
        "🎯 Понял ваш запрос! Что именно вас интересует?",
        "🔍 Ищу информацию... Можете переформулировать вопрос?",
        "🚀 Принял! Нужны дополнительные детали для ответа."
    ]
    
    return random.choice(responses)

def main_menu(user_id):
    """Главное меню с учетом прав"""
    if is_admin(user_id):
        return ReplyKeyboardMarkup([
            ["🧮 Посчитать", "⏰ Время"],
            ["🇺🇿 Новости Узбекистана", "🛠️ Админ-панель"],
            ["📊 Статистика", "👥 Пользователи"]
        ], resize_keyboard=True)
    else:
        return ReplyKeyboardMarkup([
            ["🧮 Посчитать пример", "⏰ Текущее время"],
            ["🇺🇿 Новости Узбекистана", "🤖 О боте"]
        ], resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    user_id = user.id
    
    welcome_text = f"🚀 Добро пожаловать, {user.first_name}!"
    if is_admin(user_id):
        welcome_text += "\n🛠️ Режим администратора активирован"
    
    await update.message.reply_text(
        welcome_text,
        reply_markup=main_menu(user_id)
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        text = update.message.text
        user = update.message.from_user
        user_id = user.id
        
        print(f"👤 {user.first_name} (ID: {user_id}): {text}")
        
        # Админ-команды
        if is_admin(user_id):
            if text == "🛠️ Админ-панель":
                admin_info = f"""🛠️ Админ-панель:
ID: {user_id}
Имя: {user.first_name}

Команды:
• 📊 Статистика - статистика бота
• 👥 Пользователи - список пользователей"""
                await update.message.reply_text(admin_info)
                return
                
            elif text == "📊 Статистика":
                await update.message.reply_text("📊 Статистика бота:\n• Пользователей: 15\n• Сообщений: 127\n• Онлайн: 3")
                return
                
            elif text == "👥 Пользователи":
                await update.message.reply_text("👥 Последние пользователи:\n• User1 (ID: 111)\n• User2 (ID: 222)\n• User3 (ID: 333)")
                return
        
        # Общие команды для всех
        if text in ["🧮 Посчитать", "🧮 Посчитать пример"]:
            await update.message.reply_text("💡 Напишите пример для расчета:\nНапример: 2+2, 5*8, 100/4")
            return
            
        elif text in ["⏰ Время", "⏰ Текущее время"]:
            await update.message.reply_text(f"⏰ {datetime.now().strftime('%H:%M:%S %d.%m.%Y')}")
            return
            
        elif text == "🇺🇿 Новости Узбекистана":
            response = """📰 Новости Узбекистана:
• Экономический рост: 5.8%
• Увеличение туризма: +30%
• Новые бизнес-программы
• Инвестиционные конференции

Что именно интересует?"""
            await update.message.reply_text(response)
            return
            
        elif text == "🤖 О боте":
            response = """🤖 Я - умный бот-помощник!
Мои возможности:
• Математические расчеты
• Информация о Узбекистане
• Новости и обновления
• Помощь с вопросами

Просто напишите мне вопрос!"""
            await update.message.reply_text(response)
            return
        
        # Обычные сообщения
        await update.message.reply_text("🤖 Думаю над ответом...")
        response = generate_response(text)
        await update.message.reply_text(response)
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        await update.message.reply_text("⚠️ Произошла ошибка. Попробуйте еще раз.")

def main():
    print("🚀 Запуск финальной версии бота...")
    print(f"🆔 ADMIN_ID: {ADMIN_ID}")
    
    try:
        application = Application.builder().token(BOT_TOKEN).build()
        application.add_handler(CommandHandler("start", start))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        
        print("✅ Бот успешно инициализирован!")
        print("🤖 Ожидание сообщений...")
        
        application.run_polling()
        
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")

if __name__ == "__main__":
    main()
