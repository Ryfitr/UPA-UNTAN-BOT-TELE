import os
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from handlers.handlers import start, handle_message, show_unanswered

load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")

def main():
    """Mengatur bot Telegram."""
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("unanswered", show_unanswered)) 
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()