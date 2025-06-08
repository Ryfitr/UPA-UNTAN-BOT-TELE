# 🧠 UPA UNTAN Telegram Bot

Bot Telegram berbasis Python untuk keperluan pelayanan informasi akademik UPA UNTAN. Bot ini dapat memberikan informasi FAQ, scraping konten dari Instagram, serta merekomendasikan jawaban menggunakan model AI.

Kalau kamu mau langsung pakai di README.md, bisa gunakan ini:

markdown
Copy
Edit
## 📂 Struktur Proyek

upa-untan-telegram-bot/
├── bot.py # Entry point utama bot
├── cache_store.py # Manajemen cache
├── config/ # Konfigurasi API dan variabel lingkungan
├── core/ # Logika utama: AI, scraping, formatting
├── dashboard/ # Antarmuka dashboard (streamlit)
├── database/ # Skrip DB dan file SQLite
├── handlers/ # Handler perintah bot Telegram
├── logs/ # Log aktivitas bot
├── .env # Variabel lingkungan (jangan diupload publik)
├── requirements.txt # Daftar dependensi
└── README.md # Dokumentasi proyek

Copy
Edit
Kalau kamu ingin saya bantu edit langsung isi file README.md-mu, tinggal upload file .md aslinya atau beri akses isi markdown-nya.

## 🚀 Cara Menjalankan

1. Clone repository ini
   ```bash
   git clone https://github.com/ryfitr/upa-untan-telegram-bot.git
   cd upa-untan-telegram-bot

2. Buat virtual environment & install dependensi
   ```bash
    python -m venv venv
    source venv/bin/activate   # Windows: venv\Scripts\activate
    pip install -r requirements.txt

4. Buat file .env
    Isi file .env seperti:
    ```bash
   DEEPSEEK_API_KEY=your_deepseek_key
   TELEGRAM_TOKEN=your_token_here
   ADMIN_ID==your_id_here
   OCR_SPACE_API_KEY=your_ocr_key

5. Jalankan bot
    ```bash
   python bot.py


## 📊 Dashboard
   Untuk menjalankan dashboard:
   
      streamlit run dashboard/dashboard.py

##⚙️ Fitur Utama

1. FAQ suggestion berbasis AI
2. Scraper konten dari Instagram
3. Interaksi Telegram Bot dengan command handler
4. Dashboard pemantauan berbasis Streamlit
5. Logging & penyimpanan ke SQLite
