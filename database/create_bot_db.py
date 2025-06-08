import sqlite3
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config.config import DB_PATH

def create_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS conversations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT,
    question TEXT,
    answer TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS chat_threads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT,
    role TEXT,
    message TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS unanswered (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT,
    question TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS faq (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    keyword TEXT,
    response TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS seminar (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    judul TEXT,
    penyelenggara TEXT,
    tanggal TEXT,
    lokasi TEXT,
    link TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS lowongan (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    posisi TEXT,
    perusahaan TEXT,
    deadline TEXT,
    lokasi TEXT,
    link TEXT
    )
    ''')

    conn.commit()
    conn.close()
    print("Database dan tabel berhasil dibuat.")

if __name__ == "__main__":
    create_database()
