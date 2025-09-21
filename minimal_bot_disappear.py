import os
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler
import logging

# Логирование
logging.basicConfig(level=logging.INFO)

# Токен из env
TOKEN = os.getenv("TELEGRAM_TOKEN")
if not TOKEN:
    print("Ошибка: переменная окружения TELEGRAM_TOKEN не найдена!")
    exit(1)

# --- Имитация данных ---
clients_data = [
    {"id": 1, "name": "Иван Иванов"},
    {"id": 2, "name": "Мария Петрова"},
    {"id": 3, "name": "Алексей Смирнов"}
]

requests_data = [
    {"id": 101, "title": "Заявка №1"},
    {"id": 102, "title": "Заявка №2"},
    {"id": 103, "title": "Заявка №3"}
]

stats_data = {
    "Клиенты": 3,
    "Заявки": 3,
    "Активных пользователей": 2
}

# --- Команда /start ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Бот активен ✅", reply_markup=ReplyKeyboardRemove())

    keyboard = [
        [KeyboardButton("📋 Клиенты"), KeyboardButton("📝 Заявки")],
        [KeyboardButton("📊 Статистика"), KeyboardButton("❓ Помощь")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)
    await update.message.reply_text("Выберите действие:", reply_markup=reply_markup)

# --- Обработка главных кнопок ---
async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    print("Нажата кнопка:", text)

    if text == "📋 Клиенты":
        msg = "\n".join([f"{c['id']}: {c['name']}" for c in clients_data])
        await update.message.reply_text(f"Список клиентов:\n{msg}")

    elif text == "📝 Заявки":
        # Отправляем заявки с кнопками Принять/Отказать
        for r in requests_data:
            kb = [
                [InlineKeyboardButton("✅ Принять", callback_data=f"accept_{r['id']}"),
                 InlineKeyboardButton("❌ Отказать", callback_data=f"reject_{r['id']}")]
            ]
            markup = InlineKeyboardMarkup(kb)
            await update.message.reply_text(f"Заявка: {r['title']}", reply_markup=markup)

    elif text == "📊 Статистика":
        msg = "\n".join([f"{k}: {v}" for k, v in stats_data.items()])
        await update.message.reply_text(f"Статистика:\n{msg}")

    elif text == "❓ Помощь":
        await update.message.reply_text(
            "Помощь:\n- 📋 Клиенты: список клиентов\n- 📝 Заявки: действия с заявками\n- 📊 Статистика: показатели работы\n- ❓ Помощь: эта справка"
        )

# --- Обработка кнопок Принять/Отказать ---
async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    print("Нажат callback:", query.data)

    action, req_id = query.data.split("_")
    req_id = int(req_id)

    # Найти заявку в списке
    req = next((r for r in requests_data if r['id'] == req_id), None)
    if not req:
        await query.edit_message_text("Эта заявка уже обработана ✅❌")
        return

    if action == "accept":
        await query.edit_message_text(f"Заявка {req['title']} принята ✅")
    elif action == "reject":
        await query.edit_message_text(f"Заявка {req['title']} отклонена ❌")

    # Удаляем заявку из списка, чтобы больше не показывалась
    requests_data.remove(req)

# --- Лог всех сообщений ---
async def log_all_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        print("Сообщение:", update.message.text)

# --- Создание приложения ---
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_button))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, log_all_messages))
app.add_handler(CallbackQueryHandler(callback_handler))

print("Бот запущен...")
app.run_polling()
