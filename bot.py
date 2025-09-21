import os
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("TELEGRAM_TOKEN")
API_URL = "http://127.0.0.1:8080"

if not TOKEN:
    print("Ошибка: переменная окружения TELEGRAM_TOKEN не найдена!")
    exit(1)

app = ApplicationBuilder().token(TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📋 Клиенты", callback_data="clients")],
        [InlineKeyboardButton("📝 Заявки", callback_data="requests")],
        [InlineKeyboardButton("📊 Статистика", callback_data="stats")]
    ]
    await update.message.reply_text("Бот активен ✅", reply_markup=InlineKeyboardMarkup(keyboard))

def format_request(r):
    status = r.get("status","new")
    title = r["title"]
    if status == "accepted": return f"🟢 {r['id']}: {title} [Принято]"
    if status == "rejected": return f"🔴 {r['id']}: {title} [Отклонено]"
    return f"🔵 {r['id']}: {title} [Новая]"

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    try:
        if query.data == "clients":
            res = requests.get(f"{API_URL}/api/clients").json()
            text = "📋 Клиенты:\n" + "\n".join([f"{c['id']}: {c['name']}" for c in res])
            await query.edit_message_text(text=text)

        elif query.data == "requests":
            res = requests.get(f"{API_URL}/api/requests").json()
            keyboard = []
            text_lines = []
            for r in res:
                text_lines.append(format_request(r))
                if r.get("status","new")=="new":
                    buttons = [
                        InlineKeyboardButton("✅ Принять", callback_data=f"accept_{r['id']}"),
                        InlineKeyboardButton("❌ Отказать", callback_data=f"reject_{r['id']}")
                    ]
                    keyboard.append(buttons)
            await query.edit_message_text(text="📝 Заявки:\n" + "\n".join(text_lines),
                                          reply_markup=InlineKeyboardMarkup(keyboard if keyboard else None))

        elif query.data == "stats":
            res = requests.get(f"{API_URL}/api/stats").json()
            text = "📊 Статистика:\n" + "\n".join([f"{k}: {v}" for k,v in res.items()])
            await query.edit_message_text(text=text)

        elif query.data.startswith("accept_") or query.data.startswith("reject_"):
            parts = query.data.split("_")
            action = "accepted" if parts[0]=="accept" else "rejected"
            req_id = int(parts[1])
            requests.post(f"{API_URL}/api/request/{req_id}/action", data={"action": action})
            res = requests.get(f"{API_URL}/api/requests").json()
            keyboard = []
            text_lines = []
            for r in res:
                text_lines.append(format_request(r))
                if r.get("status","new")=="new":
                    buttons = [
                        InlineKeyboardButton("✅ Принять", callback_data=f"accept_{r['id']}"),
                        InlineKeyboardButton("❌ Отказать", callback_data=f"reject_{r['id']}")
                    ]
                    keyboard.append(buttons)
            await query.edit_message_text(text="📝 Заявки:\n" + "\n".join(text_lines),
                                          reply_markup=InlineKeyboardMarkup(keyboard if keyboard else None))
    except Exception as e:
        await query.edit_message_text(f"❌ Ошибка: {e}")

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))

print("Бот запущен...")
app.run_polling()

