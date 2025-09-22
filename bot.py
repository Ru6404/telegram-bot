from aiogram import Bot, Dispatcher, types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
import asyncio

# -------------------------------
# Вставь сюда свой токен от BotFather
# -------------------------------
TELEGRAM_TOKEN = "8253068855:AAFPNJke9PYju90RgZe4ZOKOuuMSJNAs0X8"

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

# Создание клавиатуры снизу
keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📋 Заявки")],
        [KeyboardButton(text="👥 Клиенты")],
        [KeyboardButton(text="📊 Статистика")],
        [KeyboardButton(text="✅ Принять"), KeyboardButton(text="❌ Отказать")]
    ],
    resize_keyboard=True
)

# Команда /start
@dp.message()
async def start(message: types.Message):
    if message.text == "/start":
        await message.answer("Бот запущен! ✅", reply_markup=keyboard)

# Обработка кнопок
@dp.message()
async def button_handler(message: types.Message):
    if message.text == "📋 Заявки":
        await message.answer("Список заявок...")
    elif message.text == "👥 Клиенты":
        await message.answer("Список клиентов...")
    elif message.text == "📊 Статистика":
        await message.answer("Статистика...")
    elif message.text == "✅ Принять":
        await message.answer("Заявка принята ✅")
    elif message.text == "❌ Отказать":
        await message.answer("Заявка отклонена ❌")

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
