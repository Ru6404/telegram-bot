import os
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler

TOKEN = os.getenv("TELEGRAM_TOKEN")
API_URL = "http://127.0.0.1:8001"

if not TOKEN:
    print("Ошибка: переменная окружения TELEGRAM_TOKEN не найдена!")
    exit(1)

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📋 Клиенты", callback_data="clients")],
        [InlineKeyboardButton("📝 Заявки", callback_data="requests")],
        [InlineKeyboardButton("📊 Статистика", callback_data="stats")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Бот активен ✅", reply_markup=reply_markup)

# Обработка кнопок
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "clients":
        res = requests.get(f"{API_URL}/api/clients")
        clients = res.json()
        text = "📋 Клиенты:\n" + "\n".join([f"{c['id']}: {c['name']}" for c in clients])
        await query.edit_message_text(text=text, reply_markup=query.message.reply_markup)
    
    elif query.data == "requests":
        res = requests.get(f"{API_URL}/api/requests")
        requests_db = res.json()
        keyboard = []
        text_lines = []
        for r in requests_db:
            status = r.get("status","")
            text_lines.append(f"{r['id']}: {r['title']} [{status}]")
            buttons = [
                InlineKeyboardButton(f"✅ Принять", callback_data=f"accept_{r['id']}"),
                InlineKeyboardButton(f"❌ Отказать", callback_data=f"reject_{r['id']}")
            ]
            keyboard.append(buttons)
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="📝 Заявки:\n" + "\n".join(text_lines), reply_markup=reply_markup)
    
    elif query.data == "stats":
        res = requests.get(f"{API_URL}/api/stats")
        stats = res.json()
        text = "📊 Статистика:\n" + "\n".join([f"{k}: {v}" for k,v in stats.items()])
        await query.edit_message_text(text=text, reply_markup=query.message.reply_markup)
    
    elif query.data.startswith("accept_") or query.data.startswith("reject_"):
        parts = query.data.split("_")
        action = "accepted" if parts[0]=="accept" else "rejected"
        req_id = int(parts[1])
        requests.post(f"{API_URL}/api/request/{req_id}/action", params={"action": action})
        await button(update, context)  # обновляем список заявок

# Запуск бота
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))

print("Бот запущен...")
app.run_polling()
