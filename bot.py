import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from aiogram import F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from openai import AsyncOpenAI
import asyncio

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Токены
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not TELEGRAM_TOKEN:
    raise ValueError("Нет TELEGRAM_BOT_TOKEN. Задай переменную окружения!")

if not OPENAI_API_KEY:
    raise ValueError("Нет OPENAI_API_KEY. Задай переменную окружения!")

# Инициализация бота и диспетчера
bot = Bot(token=TELEGRAM_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# Инициализация OpenAI клиента
client = AsyncOpenAI(api_key=OPENAI_API_KEY)

# Клавиатура
keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Заявки")],
        [KeyboardButton(text="Клиенты")],
        [KeyboardButton(text="Статистика")],
    ],
    resize_keyboard=True
)

# Команда /start
@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer(
        "Привет! Я умный бот-помощник. Задай мне вопрос или выбери раздел из меню ниже.", 
        reply_markup=keyboard
    )

# Обработчики кнопок
@dp.message(F.text == "Заявки")
async def handle_zayavki(message: types.Message):
    await message.answer("📋 Здесь будет информация по заявкам. Раздел в разработке.")

@dp.message(F.text == "Клиенты")
async def handle_clients(message: types.Message):
    await message.answer("👥 Здесь будет информация по клиентам. Раздел в разработке.")

@dp.message(F.text == "Статистика")
async def handle_stats(message: types.Message):
    await message.answer("📊 Здесь будет статистика. Раздел в разработке.")

# Обработка текстовых сообщений (вопросов к AI)
@dp.message(F.text)
async def handle_text(message: types.Message):
    # Пропускаем кнопки - они уже обработаны выше
    if message.text in ["Заявки", "Клиенты", "Статистика"]:
        return
        
    logger.info(f"Вопрос от {message.from_user.id}: {message.text}")
    
    try:
        # Показываем статус "печатает"
        await bot.send_chat_action(message.chat.id, "typing")
        
        # Делаем запрос к OpenAI
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ты полезный ассистент. Отвечай кратко и понятно."},
                {"role": "user", "content": message.text}
            ],
            max_tokens=500,
            temperature=0.7
        )
        
        answer = response.choices[0].message.content
        logger.info(f"Ответ OpenAI: {answer[:100]}...")
        
        await message.answer(answer)
        
    except Exception as e:
        logger.error(f"Ошибка OpenAI: {e}")
        await message.answer("⚠️ Извините, произошла ошибка. Попробуйте позже.")

# Запуск бота
async def main():
    logger.info("Запуск бота...")
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Ошибка запуска: {e}")
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
