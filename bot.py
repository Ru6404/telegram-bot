import os
from aiogram import Bot, Dispatcher, F, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Router
from aiogram.utils.keyboard import ReplyKeyboardBuilder
import asyncio

# Токен берем из переменной окружения
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

if not TELEGRAM_TOKEN:
    raise ValueError("❌ TELEGRAM_TOKEN не найден! Установите его в run_bot.sh")

# Создаем объекты бота и диспетчера
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# 📌 Основные кнопки внизу
main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📋 Заявки"), KeyboardButton(text="👥 Клиенты")],
        [KeyboardButton(text="📊 Статистика")],
        [KeyboardButton(text="✅ Принять"), KeyboardButton(text="❌ Отказать")]
    ],
    resize_keyboard=True
)

# 📌 Inline кнопки внутри чата
inline_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="✅ Принять", callback_data="accept")],
        [InlineKeyboardButton(text="❌ Отказать", callback_data="decline")]
    ]
)

# 📌 Команда /start
@dp.message(F.text == "/start")
async def cmd_start(message: types.Message):
    await message.answer("👋 Привет! Я бот. Выберите действие:", reply_markup=main_kb)

# 📌 Обработчики кнопок снизу
@dp.message(F.text == "📋 Заявки")
async def show_requests(message: types.Message):
    await message.answer("📋 Здесь список заявок", reply_markup=inline_kb)

@dp.message(F.text == "👥 Клиенты")
async def show_clients(message: types.Message):
    await message.answer("👥 Здесь список клиентов")

@dp.message(F.text == "📊 Статистика")
async def show_stats(message: types.Message):
    await message.answer("📊 Здесь статистика")

@dp.message(F.text == "✅ Принять")
async def accept_from_menu(message: types.Message):
    await message.answer("✅ Заявка принята!")

@dp.message(F.text == "❌ Отказать")
async def decline_from_menu(message: types.Message):
    await message.answer("❌ Заявка отклонена!")

# 📌 Обработчики inline-кнопок
@dp.callback_query(F.data == "accept")
async def accept_request(callback: types.CallbackQuery):
    await callback.message.answer("✅ Заявка принята (inline)")
    await callback.answer()

@dp.callback_query(F.data == "decline")
async def decline_request(callback: types.CallbackQuery):
    await callback.message.answer("❌ Заявка отклонена (inline)")
    await callback.answer()

# 📌 Запуск
async def main():
    print("🤖 Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
import requests
from config import OPENAI_API_KEY

# Проверка интернета
def check_internet():
    try:
        requests.get("https://api.openai.com", timeout=3)
        return True
    except:
        return False

# Простейший офлайн-ответчик (без интернета)
def offline_answer(text: str) -> str:
    text = text.lower()
    if "привет" in text:
        return "Привет 👋 Я офлайн-бот. Интернета нет, но я всё равно с тобой."
    elif "как дела" in text:
        return "У меня всё хорошо, спасибо! 😊"
    elif "пока" in text:
        return "До встречи 👋"
    else:
        return "Сейчас я работаю без интернета, поэтому отвечаю проще."

# Онлайн-ответ через OpenAI
def online_answer(text: str) -> str:
    from openai import OpenAI
    client = OpenAI(api_key=OPENAI_API_KEY)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": text}],
        max_tokens=200,
    )
    return response.choices[0].message.content

# Универсальный обработчик
@dp.message()
async def universal_handler(message: types.Message):
    user_text = message.text
    try:
        if check_internet() and OPENAI_API_KEY:
            reply = online_answer(user_text)
        else:
            reply = offline_answer(user_text)
    except Exception as e:
        reply = f"⚠️ Ошибка: {e}"

    await message.answer(reply)
