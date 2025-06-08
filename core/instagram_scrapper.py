import instaloader
import sqlite3
import requests
import re
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config.config import DB_PATH, OCR_SPACE_API_KEY

def classify_post(text):
    if any(k in text.lower() for k in ["seminar", "webinar", "pelatihan", "workshop"]):
        return "seminar"
    elif any(k in text.lower() for k in ["lowongan", "loker", "kerja", "rekrutmen", "career"]):
        return "lowongan"
    return None

def insert_to_database(data, jenis):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    if jenis == "seminar":
        c.execute("""INSERT INTO seminar (judul, penyelenggara, tanggal, lokasi, link)
                     VALUES (?, ?, ?, ?, ?)""", (
                     data.get("judul", ""), data.get("penyelenggara", ""), data.get("tanggal", ""),
                     data.get("lokasi", ""), data.get("link", "")
                  ))

    elif jenis == "lowongan":
        c.execute("""INSERT INTO lowongan (posisi, perusahaan, deadline, lokasi, link)
                     VALUES (?, ?, ?, ?, ?)""", (
                     data.get("posisi", ""), data.get("perusahaan", ""), data.get("deadline", ""),
                     data.get("lokasi", ""), data.get("link", "")
                  ))
    conn.commit()
    conn.close()

def ocr_with_ocr_space(image_url):
    try:
        payload = {
            'url': image_url,
            'isOverlayRequired': False,
            'apikey': OCR_SPACE_API_KEY,
            'language': 'eng',
        }
        r = requests.post('https://api.ocr.space/parse/image', data=payload)
        result = r.json()
        return result['ParsedResults'][0]['ParsedText']
    except Exception as e:
        print(f"[❌ OCR.Space error]: {e}")
        return ""

def extract_posting_from_instagram(username="upa.pk2.untan", max_post=5):
    L = instaloader.Instaloader()
    profile = instaloader.Profile.from_username(L.context, username)

    for i, post in enumerate(profile.get_posts()):
        if i >= max_post:
            break
        caption = post.caption or ""
        image_url = post.url
        ocr_text = ocr_with_ocr_space(image_url)
        full_text = caption + "\n" + ocr_text
        jenis = classify_post(full_text)
        if jenis == "seminar":
            data = {
                "judul": extract_title(full_text),
                "penyelenggara": extract_by_keyword(full_text, ["oleh", "penyelenggara"]),
                "tanggal": extract_by_keyword(full_text, ["tanggal", "tgl", "waktu"]),
                "lokasi": extract_by_keyword(full_text, ["lokasi", "tempat"]),
                "link": extract_link(full_text)
            }
            insert_to_database(data, jenis)
        elif jenis == "lowongan":
            data = {
                "posisi": extract_title(full_text),
                "perusahaan": extract_by_keyword(full_text, ["perusahaan", "oleh"]),
                "deadline": extract_by_keyword(full_text, ["batas", "deadline"]),
                "lokasi": extract_by_keyword(full_text, ["lokasi", "penempatan"]),
                "link": extract_link(full_text)
            }
            insert_to_database(data, jenis)

def extract_by_keyword(text, keywords):
    for line in text.split("\n"):
        for key in keywords:
            if key in line.lower():
                parts = re.split(r":|-", line, maxsplit=1)
                if len(parts) > 1:
                    return parts[1].strip()
    return ""

def extract_link(text):
    urls = re.findall(r"(https?://[^\s]+)", text)
    return urls[0] if urls else ""

def extract_title(text):
    lines = text.strip().split("\n")
    for line in lines:
        if len(line.strip()) > 10:
            return line.strip()
    return "Tanpa Judul"
