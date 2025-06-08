import logging
import sqlite3
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import CallbackContext
from core.faq_suggester import find_similar_faq  
from core.deepseek_service import generate_response
from cache_store import cache_user_question_answer
from config.config import DB_PATH, ADMIN_ID, LOG_FILE

load_dotenv()
ADMIN_ID = os.getenv("ADMIN_ID")

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

intro_message = (
    "Saya adalah bot *UPA UNTAN (Unit Penunjang Akademik Universitas Tanjungpura)*.\n\n"
    "📚 *Apa yang bisa saya bantu?*\n"
    "- Mencari *informasi beasiswa* yang sedang dibuka.\n"
    "- Menampilkan *lomba-lomba akademik & non-akademik* yang dapat Anda ikuti.\n"
    "- Menemukan *kelas atau pelatihan* yang bermanfaat bagi mahasiswa.\n\n"
    "🔎 *Cara menggunakan bot ini:*\n"
    "- Ketik langsung pertanyaan Anda seperti sedang berbicara.\n"
    "- Contoh: 'Apa ada beasiswa tahun ini?', 'Lomba teknologi terbaru apa?', atau 'Bagaimana cara ikut pelatihan AI?'\n\n"
    "Silakan ketik sesuatu untuk memulai. 🎓"
)

async def start(update: Update, context: CallbackContext):
    user_id = update.message.chat_id
    logging.info(f"📢 User {user_id} memulai bot dengan /start")
    await update.message.reply_text(intro_message, parse_mode="Markdown")

def is_unanswered(response_text):
    keywords = ["maaf", "tidak bisa menemukan", "tidak dapat", "coba lagi"]
    return any(k in response_text.lower() for k in keywords)

def check_faq(message):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT response FROM faq WHERE ? LIKE '%' || keyword || '%'", (message,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None

async def handle_message(update: Update, context: CallbackContext):
    user_message = update.message.text.strip()
    user_id = update.message.chat_id
    logging.info(f"📩 Pesan diterima dari User {user_id}: {user_message}")
    greetings = ["halo", "hai", "tes", ".", "hello", "helo", "p"]
    waktu_salam = ["pagi", "siang", "sore", "malam"]
    if user_message.lower() in greetings or any(waktu in user_message.lower() for waktu in waktu_salam):
        await update.message.reply_text(intro_message, parse_mode="Markdown")
        return
    faq_response = check_faq(user_message.lower())
    if not faq_response:
        match = find_similar_faq(user_message)
        if match:
            faq_response = match[1]

    if faq_response:
        await update.message.reply_text(faq_response, parse_mode="Markdown")
        return

    try:
        response = generate_response(user_message, user_id)
        
        if is_unanswered(response):
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute("INSERT INTO unanswered (user_id, question) VALUES (?, ?)", 
                      (str(user_id), user_message))
            conn.commit()
            conn.close()
            logging.info(f"🚨 Pertanyaan tidak terjawab disimpan: {user_message}")

        cache_user_question_answer(user_id, user_message, response)
        await update.message.reply_text(response, parse_mode="Markdown")
        logging.info(f"📤 Bot menjawab User {user_id} dengan hasil dari DeepSeek")
    except Exception as e:
        logging.error(f"❌ Error saat menjawab User {user_id}: {str(e)}")
        await update.message.reply_text("Maaf, saya tidak bisa menjawab pertanyaan itu sekarang.", parse_mode="Markdown")

async def show_unanswered(update: Update, context: CallbackContext):
    if update.message.chat_id != int(ADMIN_ID):
        await update.message.reply_text("❌ Akses ditolak. Fitur ini hanya untuk admin.", parse_mode="Markdown")
        return
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT question, timestamp FROM unanswered ORDER BY timestamp DESC LIMIT 10")
        rows = c.fetchall()
        conn.close()
        
        if rows:
            result = "\n\n".join([f"❓ *{q}*\n🕒 {t}" for q, t in rows])
        else:
            result = "✅ Tidak ada pertanyaan yang belum terjawab."
        
        await update.message.reply_text(result, parse_mode="Markdown")
    except Exception as e:
        logging.error(f"❌ Gagal menampilkan unanswered: {str(e)}")
        await update.message.reply_text("❌ Gagal mengambil data unanswered.", parse_mode="Markdown")
