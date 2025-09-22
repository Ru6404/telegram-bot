from aiogram import Bot, Dispatcher, types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils import executor
import asyncio

# -------------------------------
# Вставь сюда свой токен от BotFather
# -------------------------------
TELEGRAM_TOKEN = "8253068855:AAFPNJke9PYju90RgZe4ZOKOuuMSJNAs0X8"

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)

# =======================
# Кнопки снизу
# =======================
keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(KeyboardButton("📋 Заявки"))
keyboard.add(KeyboardButton("👥 Клиенты"))
keyboard.add(KeyboardButton("📊 Статистика"))
keyboard.add(KeyboardButton("✅ Принять"), KeyboardButton("❌ Отказать"))

# =======================
# Команды
# =======================
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer("Бот запущен! ✅", reply_markup=keyboard)

# =======================
# Обработка кнопок
# =======================
@dp.message_handler(lambda message: message.text in ["📋 Заявки", "👥 Клиенты", "📊 Статистика",
                                                    "✅ Принять", "❌ Отказать"])
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

# =======================
# Запуск
# =======================
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
