import re
import logging

def format_response(response_text):
    logging.info("📊 Memulai proses format_response")
    
    header = "*📚 Informasi yang Tersedia:*\n\n"
    event_list = []
    temp_event = ""
    count = 0
    max_display = 5
    pendaftaran = ""

    lines = response_text.split("\n")
    
    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Deteksi awal event baru
        if re.match(r"^(#\s*)?\d{1,2}\.\s", line):
            if count >= max_display:
                break

            # Simpan event sebelumnya jika ada
            if temp_event:
                if pendaftaran:
                    temp_event += f"📅 _Pendaftaran:_ {pendaftaran}\n"
                event_list.append(temp_event.strip())
                temp_event = ""
                pendaftaran = ""

            # Mulai event baru
            nama_event = re.sub(r"^(#\s*)?\d{1,2}\.\s", '', line).strip()
            count += 1
            temp_event = f"*{count}. {nama_event}*\n"

        elif "Pendaftaran" in line or "Periode" in line:
            pendaftaran = line.split(":", 1)[-1].strip()

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

        elif "Situs:" in line or "Sumber" in line or "Link:" in line:
            link = line.split(":", 1)[-1].strip()
            if link.startswith("http"):
                temp_event += f"🔗 [Kunjungi Link]({link})\n"
            else:
                temp_event += f"🔗 _Link:_ {link}\n"

    # Simpan event terakhir (jika belum disimpan)
    if temp_event:
        if pendaftaran:
            temp_event += f"📅 _Pendaftaran:_ {pendaftaran}\n"
        event_list.append(temp_event.strip())

    # Tambahkan info jika melebihi batas tampilan
    if count >= max_display:
        event_list.append("❗ *Masih ada informasi lain yang tersedia.*\n_Ketik 'Lihat lebih banyak' untuk melihat semua._")

    logging.info("🎯 Format respons selesai")
    return header + "\n\n".join(event_list)
