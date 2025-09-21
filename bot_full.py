import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# =================== Токен ===================
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
if not TELEGRAM_TOKEN:
    print("❌ TELEGRAM_TOKEN не найден!")
    exit(1)

# =================== Команда /start ===================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Создаем inline-кнопки
    keyboard = [
        [InlineKeyboardButton("👤 Клиенты", callback_data="clients")],
        [InlineKeyboardButton("📊 Статистика", callback_data="stats")],
        [InlineKeyboardButton("✅ Принять", callback_data="accept"),
         InlineKeyboardButton("❌ Отказать", callback_data="reject")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Выбери действие:", reply_markup=reply_markup)

# =================== Обработка кнопок ===================
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # Подтверждаем Telegram

    if query.data == "clients":
        await query.edit_message_text("📋 Список клиентов:\n1. Иван\n2. Мария")
    elif query.data == "stats":
        await query.edit_message_text("📊 Статистика пока пустая")
    elif query.data == "accept":
        await query.edit_message_text("✅ Вы приняли заявку")
    elif query.data == "reject":
        await query.edit_message_text("❌ Вы отклонили заявку")

# =================== Запуск бота ===================
def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))

    print("✅ Бот запущен и готов к работе")
    app.run_polling()

if __name__ == "__main__":
    main()
