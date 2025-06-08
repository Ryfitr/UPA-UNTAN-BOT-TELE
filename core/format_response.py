import logging

def format_response(response_text):
    """Memformat ulang respons dari DeepSeek agar rapi menggunakan Markdown Telegram (tanpa escape)."""
    logging.info("📊 Memulai proses format_response (NO ESCAPE Mode)")
    header = "*📚 Informasi yang Tersedia:*\n\n"
    event_list = []
    temp_event = ""
    count = 0
    max_display = 5

    lines = response_text.split("\n")

    for line in lines:
        line = line.strip()
        if not line:
            continue

        if line.startswith("###") or line[0].isdigit():
            if count >= max_display:
                break
            if temp_event:
                event_list.append(temp_event.strip())
            current_event = line.replace('###', '').strip()
            temp_event = f"*{count+1}. {current_event}*\n"
            count += 1

        elif "Penyelenggara" in line or "Organisasi" in line:
            penyelenggara = line.split(":", 1)[-1].strip()
            temp_event += f"🏛 _Penyelenggara:_ {penyelenggara}\n"

        elif "Bidang" in line or "Kategori" in line:
            bidang = line.split(":", 1)[-1].strip()
            temp_event += f"🛠 _Bidang:_ {bidang}\n"

        elif "Lokasi" in line:
            lokasi = line.split(":", 1)[-1].strip()
            temp_event += f"📍 _Lokasi:_ {lokasi}\n"

        elif "Pelaksanaan" in line:
            pelaksanaan = line.split(":", 1)[-1].strip()
            temp_event += f"⏳ _Pelaksanaan:_ {pelaksanaan}\n"

        elif "Jenjang" in line:
            jenjang = line.split(":", 1)[-1].strip()
            temp_event += f"🎓 _Jenjang:_ {jenjang}\n"

        elif "Pendaftaran" in line or "Periode" in line:
            pendaftaran = line.split(":", 1)[-1].strip()
            temp_event += f"📅 _Pendaftaran:_ {pendaftaran}\n"

        elif "Situs:" in line or "Sumber" in line or "Link:" in line:
            link = line.split(":", 1)[-1].strip()
            if link.startswith("http"):
                temp_event += f"🔗 [Kunjungi Link]({link})\n"
            else:
                temp_event += f"🔗 _Link:_ {link}\n"

    if temp_event:
        event_list.append(temp_event.strip())

    if count >= max_display:
        event_list.append("\n❗ *Masih ada informasi lain yang tersedia.*\n_Ketik 'Lihat lebih banyak' untuk melihat semua._")
    
    logging.info("🎯 Format respons selesai (NO ESCAPE Mode)")
    return header + "\n\n".join(event_list)
