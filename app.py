import threading
import asyncio
from fastapi import FastAPI
import uvicorn
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
)
import os

# =================== FASTAPI ===================
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/api/clients")
def get_clients():
    return [
        {"id": 1, "name": "Иван"},
        {"id": 2, "name": "Мария"}
    ]

def run_api():
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=False)

# =================== TELEGRAM BOT ===================
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("👤 Клиенты", callback_data="clients")],
        [InlineKeyboardButton("📊 Статистика", callback_data="stats")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Привет! Выбери опцию:", reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "clients":
        await query.edit_message_text("📋 Список клиентов:\n1. Иван\n2. Мария")
    elif query.data == "stats":
        await query.edit_message_text("📊 Статистика пока пустая.")

def run_bot():
    if not TELEGRAM_TOKEN:
        print("❌ Ошибка: TELEGRAM_TOKEN не найден!")
        return
    app_telegram = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app_telegram.add_handler(CommandHandler("start", start))
    app_telegram.add_handler(CallbackQueryHandler(button))
    app_telegram.run_polling()

# =================== MAIN ===================
if __name__ == "__main__":
    # Запускаем API в отдельном потоке
    threading.Thread(target=run_api, daemon=True).start()
    # Запускаем бота
    run_bot()
