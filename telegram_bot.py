from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import asyncio
import requests

class QuantumTelegramBot:
    def __init__(self, token):
        self.token = token
        self.app = Application.builder().token(token).build()
        self.setup_handlers()
    
    def setup_handlers(self):
        self.app.add_handler(CommandHandler("start", self.start))
        self.app.add_handler(CommandHandler("status", self.status))
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
    
    async def start(self, update: Update, context):
        await update.message.reply_text("🚀 Quantum System 2025 Bot активирован!\nИспользуйте /status для проверки системы")
    
    async def status(self, update: Update, context):
        try:
            response = requests.get("http://localhost:8000/health", timeout=5)
            status_data = response.json()
            await update.message.reply_text(f"✅ Система работает:\n{status_data}")
        except:
            await update.message.reply_text("❌ Система не отвечает")
    
    async def handle_message(self, update: Update, context):
        text = update.message.text
        await update.message.reply_text(f"🔮 Принято: {text}\n\nОтправьте /status для проверки системы")
    
    async def run(self):
        print("🤖 Telegram Bot запускается...")
        await self.app.run_polling()

# ЗАМЕНИТЕ НА ВАШ ТОКЕН!
TOKEN = "ВАШ_ТОКЕН_ЗДЕСЬ"

if __name__ == "__main__":
    bot = QuantumTelegramBot(TOKEN)
    asyncio.run(bot.run())
