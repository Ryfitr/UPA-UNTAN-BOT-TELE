import streamlit as st
import sqlite3
import pandas as pd
from io import BytesIO
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config.config import DB_PATH
from core.faq_suggester import group_unanswered_questions  

st.set_page_config(page_title="📊 Dashboard Bot UPA UNTAN", layout="wide")
st.title("📊 Dashboard Bot UPA UNTAN")

def load_table(table_name):
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"❌ Gagal membaca tabel `{table_name}`: {e}")
        return pd.DataFrame()

def export_to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Data')
    output.seek(0)
    return output

def insert_faq(keyword, response):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO faq (keyword, response) VALUES (?, ?)", (keyword, response))
    conn.commit()
    conn.close()

def update_faq(faq_id, keyword, response):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE faq SET keyword = ?, response = ? WHERE id = ?", (keyword, response, faq_id))
    conn.commit()
    conn.close()

def insert_seminar(judul, penyelenggara, tanggal, lokasi, link):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO seminar (judul, penyelenggara, tanggal, lokasi, link) VALUES (?, ?, ?, ?, ?)",
              (judul, penyelenggara, tanggal, lokasi, link))
    conn.commit()
    conn.close()

def insert_lowongan(posisi, perusahaan, deadline, lokasi, link):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO lowongan (posisi, perusahaan, deadline, lokasi, link) VALUES (?, ?, ?, ?, ?)",
              (posisi, perusahaan, deadline, lokasi, link))
    conn.commit()
    conn.close()

# ================== UI ==================
table_choice = st.sidebar.selectbox(
    "📂 Pilih Tabel",
    ("conversations", "unanswered", "faq", "seminar", "lowongan")
)

st.markdown(f"### Tabel: `{table_choice}`")
df = load_table(table_choice)

if not df.empty:
    st.dataframe(df, use_container_width=True)
    st.download_button(
        label="⬇️ Download Excel",
        data=export_to_excel(df),
        file_name=f"{table_choice}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
else:
    st.warning("⚠️ Tidak ada data yang bisa ditampilkan.")

if table_choice == "conversations" and 'user_id' in df.columns:
    st.markdown("#### 🔍 Statistik Pengguna:")
    user_counts = df['user_id'].value_counts().reset_index()
    user_counts.columns = ['User ID', 'Jumlah Pertanyaan']
    st.dataframe(user_counts)

if table_choice == "unanswered":
    st.markdown("### ✏️ Jawab Pertanyaan Unanswered")

    if not df.empty:
        selected_row = st.selectbox("Pilih pertanyaan:", df['id'])
        selected_data = df[df['id'] == selected_row].iloc[0]

        st.write(f"**Pertanyaan:** {selected_data['question']}")
        with st.form("jawab_unanswered"):
            keyword = st.text_input("Keyword untuk FAQ", value=selected_data['question'])
            jawaban = st.text_area("Jawaban")
            tambah_faq = st.form_submit_button("Simpan sebagai FAQ")

            if tambah_faq and keyword and jawaban:
                insert_faq(keyword.strip(), jawaban.strip())

                # hapus dari unanswered
                conn = sqlite3.connect(DB_PATH)
                c = conn.cursor()
                c.execute("DELETE FROM unanswered WHERE id = ?", (selected_row,))
                conn.commit()
                conn.close()
                st.success("✅ Pertanyaan dijadikan FAQ dan dihapus dari unanswered.")
    else:
        st.info("Belum ada pertanyaan tidak terjawab.")


if table_choice == "faq":
    st.markdown("### ➕ Tambah FAQ Baru")
    with st.form("faq_form"):
        keyword = st.text_input("Keyword")
        response = st.text_area("Jawaban")
        submitted = st.form_submit_button("Tambah")
        if submitted and keyword and response:
            insert_faq(keyword.strip(), response.strip())
            st.success("✅ FAQ berhasil ditambahkan!")

    if not df.empty:
        st.markdown("### ✏️ Edit FAQ")
        selected = st.selectbox("Pilih FAQ:", df['id'])
        selected_data = df[df['id'] == selected].iloc[0]
        with st.form("edit_faq_form"):
            new_keyword = st.text_input("Keyword", selected_data['keyword'])
            new_response = st.text_area("Jawaban", selected_data['response'])
            submitted_edit = st.form_submit_button("Simpan Perubahan")
            if submitted_edit:
                update_faq(selected, new_keyword.strip(), new_response.strip())
                st.success("✅ FAQ berhasil diperbarui!")

    st.markdown("### 🤖 Rekomendasi FAQ Otomatis")
    grouped = group_unanswered_questions()
    if grouped:
        for idx, group in enumerate(grouped):
            st.markdown(f"**Kelompok {idx+1}:**")
            for q in group:
                st.write(f"- {q}")
    else:
        st.info("Belum ada pertanyaan serupa di unanswered.")

if table_choice == "seminar":
    st.markdown("### ➕ Tambah Seminar Baru")
    with st.form("seminar_form"):
        judul = st.text_input("Judul Seminar")
        penyelenggara = st.text_input("Penyelenggara")
        tanggal = st.date_input("Tanggal")
        lokasi = st.text_input("Lokasi")
        link = st.text_input("Link (opsional)")
        submitted = st.form_submit_button("Tambah")
        if submitted:
            insert_seminar(judul, penyelenggara, tanggal.strftime("%Y-%m-%d"), lokasi, link)
            st.success("✅ Seminar berhasil ditambahkan!")

if table_choice == "lowongan":
    st.markdown("### ➕ Tambah Lowongan Baru")
    with st.form("lowongan_form"):
        posisi = st.text_input("Posisi")
        perusahaan = st.text_input("Perusahaan")
        deadline = st.date_input("Deadline")
        lokasi = st.text_input("Lokasi")
        link = st.text_input("Link (opsional)")
        submitted = st.form_submit_button("Tambah")
        if submitted:
            insert_lowongan(posisi, perusahaan, deadline.strftime("%Y-%m-%d"), lokasi, link)
            st.success("✅ Lowongan berhasil ditambahkan!")
