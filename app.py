import streamlit as st
import yt_dlp
import os
import json

# Configurare pagină
st.set_page_config(page_title="YT Clipper Pro", page_icon="✂️")
st.title("✂️ YouTube Automatic Clipper")

DB_FILE = "database.json"

# Funcție pentru memorarea fișierelor selectate
def load_data():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return []

def save_data(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f)

# Inițializare listă
if 'clips' not in st.session_state:
    st.session_state.clips = load_data()

# --- MOTORUL DE DESCĂRCARE (V3 - Safe Mode) ---
def download_clip(url, start, end):
    if not os.path.exists("downloads"):
        os.makedirs("downloads")
    
    output = f"downloads/clip_{start}_{end}.mp4"
    
    ydl_opts = {
        'format': 'mp4/best', # Cel mai compatibil format
        'quiet': True,
        'nocheckcertificate': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'download_sections': [{'start_time': start, 'end_time': end}],
        'force_keyframes_at_cuts': True,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return output

# --- INTERFAȚA ---
with st.sidebar:
    st.header("Adaugă Clip Nou")
    new_url = st.text_input("Link YouTube")
    seg_time = st.number_input("Secunde per segment", 5, 60, 15)
    
    if st.button("Salvează în listă"):
        if new_url:
            st.session_state.clips.append({"url": new_url, "seg": seg_time})
            save_data(st.session_state.clips)
            st.success("Salvat!")

# Afișare Istoric (Memorie)
st.subheader("📋 Clipurile tale salvate")
for idx, item in enumerate(st.session_state.clips):
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write(f"**{idx+1}.** {item['url']} ({item['seg']}s)")
    with col2:
        if st.button(f"Taie {idx+1}"):
            try:
                with st.spinner("Se taie..."):
                    path = download_clip(item['url'], 0, item['seg'])
                    with open(path, "rb") as f:
                        st.download_button("📥 Descarcă", f, file_name=f"clip_{idx}.mp4")
            except Exception as e:
                st.error("YouTube blochează serverul (403).")

if st.button("Șterge tot istoricul"):
    st.session_state.clips = []
    save_data([])
    st.rerun()
