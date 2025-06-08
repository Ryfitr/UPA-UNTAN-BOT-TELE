import os
import sqlite3
import requests
import datetime
import pytz
import logging
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config.config import DB_PATH, LOG_FILE, ADMIN_ID
from core.format_response import format_response

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
API_URL = "https://api.deepseek.com/v1/chat/completions"

# ==== DATABASE HANDLING ====
def get_chat_history(user_id, limit=10):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT role, message FROM chat_threads WHERE user_id=? ORDER BY timestamp DESC LIMIT ?", (str(user_id), limit))
    rows = c.fetchall()
    conn.close()
    return [{"role": role, "content": msg} for role, msg in reversed(rows)]

def store_chat_history(user_id, messages):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # Clear previous
    c.execute("DELETE FROM chat_threads WHERE user_id=?", (str(user_id),))
    # Insert new
    for msg in messages:
        c.execute("INSERT INTO chat_threads (user_id, role, message) VALUES (?, ?, ?)", (str(user_id), msg["role"], msg["content"]))
    conn.commit()
    conn.close()

def get_current_time():
    tz = pytz.timezone("Asia/Jakarta")
    now = datetime.datetime.now(tz)
    return now.strftime("%d %B %Y, %H:%M:%S %Z")

def generate_response(user_message, user_id):
    """
    Membuat balasan berdasarkan history chat dan pesan baru,
    dengan template prompt agar hasil lebih terstruktur.
    """
    try:
        today = datetime.datetime.today().strftime("%Y-%m-%d")
        structured_instruction = f"""
        Anggap kamu adalah asisten untuk mahasiswa universitas.
        Pertanyaannya adalah: "{user_message}"
        
        Jawablah dalam bahasa Indonesia.
        Hanya tampilkan informasi yang masih berlaku dan relevan untuk jenjang mahasiswa (S1, S2, atau S3).
        Jangan tampilkan informasi atau istilah untuk pelajar SD, SMP, atau SMA.
        Jika pertanyaan berkaitan dengan lomba, beasiswa, pelatihan, atau event, tampilkan hanya yang aktif setelah tanggal {today}.
        
        Jika informasi berupa daftar event, gunakan format seperti ini:
        
        1. [Nama Event]
        Pendaftaran: ...
        Penyelenggara: ...
        Bidang: ...
        Lokasi: ...
        Pelaksanaan: ...
        Jenjang: ...
        Link: ...
        """.strip()

        history = [
        {"role": "system", "content": structured_instruction},
        {"role": "user", "content": user_message}
        ]

        payload = {
            "model": "deepseek-chat",
            "messages": history,
            "temperature": 0.7,
            "max_tokens": 1000
        }

        headers = {
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        }

        logging.info(f"🔵 Sending to DeepSeek API for user {user_id} with payload size {len(history)}")
        response = requests.post(API_URL, json=payload, headers=headers)

        if response.status_code == 200:
            bot_reply = response.json()["choices"][0]["message"]["content"]
            bot_reply_clean = format_response(bot_reply)
            history.append({"role": "assistant", "content": bot_reply})
            store_chat_history(user_id, history[-10:])

            logging.info(f"✅ Response berhasil untuk user {user_id}")
            return bot_reply_clean
        else:
            logging.error(f"❌ DeepSeek API Error {response.status_code}: {response.text}")
            return "Maaf, saya tidak dapat memproses permintaan Anda saat ini."

    except Exception as e:
        logging.error(f"❌ Exception di generate_response: {str(e)}")
        return "Terjadi kesalahan internal pada sistem. Mohon coba lagi nanti."

    
def reset_chat(user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM chat_threads WHERE user_id=?", (str(user_id),))
    conn.commit()
    conn.close()
    logging.info(f"🔄 Chat history reset untuk user {user_id}")
    return "🔄 Riwayat chat Anda telah direset."
