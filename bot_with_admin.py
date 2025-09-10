import os
import random
import re
from datetime import datetime
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = "8253068855:AAFPNJke9PYju90RgZe4ZOKOuuMSJNAs0X8"
ADMIN_ID = 5569793273  

def is_admin(user_id):
    return user_id == ADMIN_ID

def calculate_math(expression):
    try:
        if not re.match(r'^[\d\s\+\-\*\/\(\)\.]+$', expression):
            return None
        if any(op in expression for op in ['**', '//', '%', '&', '|', '^', '~', '=']):
            return None
        result = eval(expression, {"__builtins__": None}, {})
        return result
    except:
        return None

def generate_response(message):
    message_lower = message.lower()
    
    if any(word in message_lower for word in ['привет', 'здравств', 'hello', 'hi']):
        return "👋 Привет! Я бот-помощник. Спросите меня о чем угодно!"
    
    if any(word in message_lower for word in ['что ты можешь', 'возможности', 'функции']):
        return """🤖 Я могу:
• 🧮 Решать примеры: 2+2, 5*8
• ⏰ Показывать время
• 🇺🇿 Рассказывать об Узбекистане
• 📰 Давать новости

Попробуйте: "Сколько будет 15*20" или "Новости Узбекистана\""""
    
    if any(word in message_lower for word in ['узбекистан', 'узбек', 'ташкент']):
        return """🇺🇿 Узбекистан:
Столица: Ташкент
Население: 35 млн человек
Экономика: рост 5.8%
Туризм: +30% в этом году

Что именно интересует?"""
    
    if 'новости' in message_lower and 'узбек' in message_lower:
        return """📰 Новости Узбекистана:
• Экономика растет на 5.8%
• Туризм увеличился на 30%
• Новые инвестиционные проекты

Уточните тему для подробностей!"""
    
    if any(word in message_lower for word in ['время', 'который час', 'дата']):
        return f"⏰ Сейчас: {datetime.now().strftime('%H:%M:%S %d.%m.%Y')}"
    
    math_match = re.search(r'(\d+[\+\-\*\/]\d+)|(посчитай|сколько будет)\s+(.+)', message)
    if math_match:
        expr = math_match.group(1) or math_match.group(3)
        if expr:
            result = calculate_math(expr)
            if result is not None:
                return f"🧮 Результат: {expr} = {result}"
            else:
                return "❌ Не могу решить этот пример"
    
    if any(word in message_lower for word in ['переведи', 'translat', 'перевод']):
        return "🌍 Напишите: 'переведи [слово] на [язык]'"
    
    responses = [
        "🤔 Интересный вопрос! Уточните детали?",
        "💡 Хорошо, я подумаю над этим. Что именно интересует?",
        "🎯 Понял ваш запрос! Нужны дополнительные детали",
        "🔍 Ищу информацию... Можете переформулировать вопрос?",
        "🚀 Принял! Задайте более конкретный вопрос"
    ]
    
    return random.choice(responses)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    user_id = user.id
    
    # Разные меню для админа и пользователей
    if is_admin(user_id):
        keyboard = [
            ["🧮 Посчитать", "⏰ Время"],
            ["🇺🇿 Новости", "🛠️ Админ"],
            ["📊 Статистика", "👥 Пользователи"]
        ]
    else:
        keyboard = [
            ["🧮 Посчитать пример", "⏰ Текущее время"],
            ["🇺🇿 Новости Узбекистана", "🤖 О боте"]
        ]
    
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    welcome_text = f"🚀 Добро пожаловать, {user.first_name}!"
    if is_admin(user_id):
        welcome_text += "\n🛠️ Режим администратора активирован"
    
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        text = update.message.text
        user = update.message.from_user
        user_id = user.id
        
        print(f"📩 {user.first_name} (ID: {user_id}): {text}")
        
        # Админ-команды
        if is_admin(user_id):
            if text == "🛠️ Админ":
                admin_info = f"""🛠️ Админ-панель:
ID: {user_id}
Имя: {user.first_name}

Команды:
/users - список пользователей
/stats - статистика
/broadcast - рассылка"""
                await update.message.reply_text(admin_info)
                return
                
            elif text == "📊 Статистика":
                await update.message.reply_text("📊 Статистика бота:\nПользователей: 15\nСообщений: 127\nОнлайн: 3")
                return
                
            elif text == "👥 Пользователи":
                await update.message.reply_text("👥 Последние пользователи:\n• User1 (ID: 111)\n• User2 (ID: 222)\n• User3 (ID: 333)")
                return
        
        # Общие команды для всех
        if text == "🧮 Посчитать" or text == "🧮 Посчитать пример":
            await update.message.reply_text("💡 Напишите пример для расчета:\nНапример: 2+2, 5*8, 100/4")
            return
            
        elif text == "⏰ Время" or text == "⏰ Текущее время":
            await update.message.reply_text(f"⏰ {datetime.now().strftime('%H:%M:%S %d.%m.%Y')}")
            return
            
        elif text == "🇺🇿 Новости" or text == "🇺🇿 Новости Узбекистана":
            response = """📰 Новости Узбекистана:
• Экономический рост: 5.8%
• Увеличение туризма: +30%
• Новые бизнес-программы

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
    print("🚀 Запуск бота с админ-панелью...")
    
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
