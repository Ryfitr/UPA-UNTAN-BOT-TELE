import os
from dotenv import load_dotenv

load_dotenv()
# 🔐 Admin Telegram ID
ADMIN_ID = int(os.getenv("ADMIN_ID", 0))  # Default 0 kalau tidak ada

# 🔑 API Key untuk DeepSeek
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")

# 🗂 Path ke database utama
DB_PATH = "database/bot_data.db"

# 📝 Path ke log file
LOG_FILE = "logs/bot.log"

#OCR.SPACE API
OCR_SPACE_API_KEY = os.getenv("OCR_SPACE_API_KEY", "")