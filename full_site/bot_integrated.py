import os
import requests
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = os.getenv("TELEGRAM_TOKEN")
SITE_URL = os.getenv("SITE_URL", "http://localhost:8000")

if not TOKEN:
    print("Ошибка: TELEGRAM_TOKEN не найден!")
    exit(1)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Бот активен ✅")

    keyboard = [
        [KeyboardButton("📋 Клиенты"), KeyboardButton("📝 Заявки")],
        [KeyboardButton("📊 Статистика"), KeyboardButton("❓ Помощь")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)
    await update.message.reply_text("Выберите действие:", reply_markup=reply_markup)

async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    logger.info(f"Нажата кнопка: {text}")

    try:
        if text == "📋 Клиенты":
            r = requests.get(f"{SITE_URL}/api/clients")
            r.raise_for_status()
            data = r.json()
            msg = "\n".join([f"{c['id']}: {c['name']}" for c in data])
            await update.message.reply_text(f"Список клиентов:\n{msg}")
        elif text == "📝 Заявки":
            r = requests.get(f"{SITE_URL}/api/requests")
            r.raise_for_status()
            data = r.json()
            for req in data:
                kb = [
                    [InlineKeyboardButton("✅ Принять", callback_data=f"accept_{req['id']}"),
                     InlineKeyboardButton("❌ Отказать", callback_data=f"reject_{req['id']}")]
                ]
                markup = InlineKeyboardMarkup(kb)
                await update.message.reply_text(f"Заявка: {req['title']}", reply_markup=markup)
        elif text == "📊 Статистика":
            r = requests.get(f"{SITE_URL}/api/stats")
            r.raise_for_status()
            stats = r.json()
            msg = "\n".join([f"{k}: {v}" for k, v in stats.items()])
            await update.message.reply_text(f"Статистика:\n{msg}")
        elif text == "❓ Помощь":
            await update.message.reply_text(
                "Помощь:\n- 📋 Клиенты\n- 📝 Заявки\n- 📊 Статистика\n- ❓ Помощь"
            )
        else:
            await update.message.reply_text("Неизвестная кнопка ❌")
    except Exception as e:
        logger.error(f"Ошибка при обработке кнопки {text}: {e}")
        await update.message.reply_text(f"Ошибка при запросе данных: {e}")

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    action, req_id = query.data.split("_")
    req_id = int(req_id)
    try:
        r = requests.post(f"{SITE_URL}/api/request/{req_id}/action?action={'accepted' if action=='accept' else 'rejected'}")
        r.raise_for_status()
        await query.edit_message_text(f"Заявка {req_id} {'принята ✅' if action=='accept' else 'отклонена ❌'}")
        logger.info(f"Заявка {req_id} обновлена: {'accepted' if action=='accept' else 'rejected'}")
    except Exception as e:
        logger.error(f"Ошибка при обновлении заявки {req_id}: {e}")
        await query.edit_message_text(f"Ошибка при обновлении заявки {req_id}: {e}")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_button))
app.add_handler(CallbackQueryHandler(callback_handler))

print("Бот запущен...")
app.run_polling()
