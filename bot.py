import os
import logging
from datetime import datetime

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TelegramBot:
    def __init__(self):
        self.bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.bot = Bot(token=self.bot_token)
        self.dp = Dispatcher()
    
    async def process_message(self, message: str, user_id: int) -> str:
        """Обработка входящего сообщения с интеллектуальными ответами"""
        message_lower = message.lower().strip()
        
        # 1. Математические вычисления - ПЕРВЫЙ ПРИОРИТЕТ
        if any(op in message for op in ['+', '-', '*', '/', '×', '÷']) and any(c.isdigit() for c in message):
            try:
                # Очищаем сообщение от лишних слов
                clean_msg = message.lower()
                for word in ['посчитай', 'вычисли', 'сколько будет', 'реши']:
                    clean_msg = clean_msg.replace(word, '')
                clean_msg = clean_msg.strip()
                
                # УСИЛЕННАЯ проверка безопасности
                safe_chars = '0123456789+-*/(). '
                forbidden_words = ['import', 'exec', 'open', 'sys', 'os', '__']
                
                if (all(c in safe_chars for c in clean_msg) and 
                    not any(word in clean_msg for word in forbidden_words)):
                    result = eval(clean_msg)
                    return f"🔢 Результат: {clean_msg} = {result}"
                else:
                    return "❌ Недопустимое математическое выражение"
            except ZeroDivisionError:
                return "❌ Ошибка: деление на ноль"
            except:
                return "❌ Не могу вычислить это выражение"
        
        # 2. Приветствия
        if any(word in message_lower for word in ['привет', 'hello', 'hi', 'здравствуй', 'добрый день', 'добрый вечер', 'начать', 'start']):
            return "Привет! 😊 Рад вас видеть! Чем могу помочь?"
        
        # 3. Явные команды вычисления
        elif any(word in message_lower for word in ['посчитай', 'вычисли', 'сколько будет', 'реши пример']):
            return "Напишите математический пример, например: 2+2 или 10*5"
        
        # 4. Вопросы о возможностях
        elif any(word in message_lower for word in ['что ты умеешь', 'твои возможности', 'команды', 'help', 'помощь']):
            return "🤖 Я умею: решать примеры (2+2), говорить время, отвечать на вопросы!"
        
        # 5. Вопросы о боте
        elif any(word in message_lower for word in ['кто ты', 'что ты', 'твое имя', 'как тебя зовут']):
            return "Я бот-помощник! 🤖 Создан для общения и решения задач."
        
        # 6. Благодарности
        elif any(word in message_lower for word in ['спасибо', 'благодарю', 'thanks', 'thank you']):
            return "Пожалуйста! 😊 Рад помочь!"
        
        # 7. Прощания
        elif any(word in message_lower for word in ['пока', 'до свидания', 'goodbye', 'see you', 'до встречи']):
            return "До свидания! 👋"
        
        # 8. Время и дата
        elif any(word in message_lower for word in ['время', 'дата', 'который час', 'сколько времени', 'какое число']):
            current_time = datetime.now().strftime("%H:%M:%S")
            current_date = datetime.now().strftime("%d.%m.%Y")
            return f"🕐 Время: {current_time}\n📅 Дата: {current_date}"
        
        # 9. Как дела
        elif 'как дела' in message_lower:
            return "Отлично! Работаю. 😊 А у вас?"
        
        # 10. Что делаешь
        elif 'что делаешь' in message_lower:
            return "Помогаю пользователям! 💻"
        
        # 11. Погода
        elif any(word in message_lower for word in ['погода', 'weather']):
            return "🌤️ Функция погоды пока не доступна"
        
        # 12. Шутки
        elif any(word in message_lower for word in ['шутка', 'анекдот', 'расскажи шутку']):
            return "Почему программисты так плохо танцуют? У них нет алгоритма! 💃"
        
        # 13. Вопросы
        elif message_lower.endswith('?'):
            if 'как' in message_lower:
                return "Не знаю как ответить на этот вопрос 🤔"
            elif 'почему' in message_lower:
                return "Интересный вопрос! Не могу ответить 😊"
            else:
                return "Не понимаю вопроса. Спросите что-то проще!"
        
        # 14. Короткие сообщения
        elif len(message) < 3:
            return "Не понял. Напишите подробнее?"
        
        # 15. Сообщения с числами
        elif any(c.isdigit() for c in message):
            return "Вижу числа! Хотите что-то посчитать? Напишите пример с +, -, *, /"
        
        # 16. АБСОЛЮТНО ВСЁ ОСТАЛЬНОЕ
        else:
            return "Не совсем понял. Можете задать вопрос или пример? 🤖"

    async def start_bot(self):
        """Запуск бота"""
        await self.dp.start_polling(self.bot)

# Запуск бота
if __name__ == "__main__":
    bot = TelegramBot()
    asyncio.run(bot.start_bot())
