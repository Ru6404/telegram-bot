import os
import asyncio
import nest_asyncio
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# ------------------ исправление для Termux / Jupyter / asyncio ------------------
nest_asyncio.apply()

# ------------------ Настройки ------------------
TOKEN = os.getenv("TELEGRAM_TOKEN")
if not TOKEN:
    print("❌ TELEGRAM_TOKEN не найден!")
    exit(1)

app_fastapi = FastAPI()
clients_db = [{"id":1,"name":"Иван"}, {"id":2,"name":"Мария"}]

# ------------------ Endpoints сайта ------------------
@app_fastapi.get("/api/clients")
async def get_clients():
    return JSONResponse(content=clients_db)

@app_fastapi.get("/")
async def home():
    return {"message": "Hello World"}

# ------------------ Telegram бот ------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("👤 Клиенты", callback_data="clients")],
        [InlineKeyboardButton("📊 Статистика", callback_data="stats")],
        [InlineKeyboardButton("✅ Принять", callback_data="accept"),
         InlineKeyboardButton("❌ Отказать", callback_data="reject")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Выбери действие:", reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "clients":
        await query.edit_message_text(f"📋 Клиенты:\n" + "\n".join([c["name"] for c in clients_db]))
    elif query.data == "stats":
        await query.edit_message_text("📊 Статистика пока пустая")
    elif query.data == "accept":
        await query.edit_message_text("✅ Вы приняли заявку")
    elif query.data == "reject":
        await query.edit_message_text("❌ Вы отклонили заявку")

async def start_bot():
    app_bot = ApplicationBuilder().token(TOKEN).build()
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(CallbackQueryHandler(button))
    print("✅ Бот запущен")
    await app_bot.run_polling()

# ------------------ Запуск FastAPI + Бота ------------------
async def main():
    import uvicorn
    config = uvicorn.Config(app_fastapi, host="0.0.0.0", port=8000, log_level="info")
    server = uvicorn.Server(config)
    asyncio.create_task(server.serve())  # FastAPI сервер в фоне
    await start_bot()  # Бот запускается в основном потоке

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())

