import streamlit as st
import yt_dlp
import os
import json

st.set_page_config(page_title="YouTube Clipper Pro", page_icon="✂️")
st.title("✂️ YouTube Automatic Clipper")

# Folder pentru rezultate
if not os.path.exists("downloads"):
    os.makedirs("downloads")

# Funcție pentru tăiere
def download_and_cut(url, start, end, output_name):
    outtmpl = f"downloads/{output_name}.%(ext)s"
    
    # Comanda specială pentru tăiere fără a descărca tot clipul
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': outtmpl,
        'download_sections': [{
            'start_time': sum(x * int(t) for x, t in zip([3600, 60, 1], start.split(':'))),
            'end_time': sum(x * int(t) for x, t in zip([3600, 60, 1], end.split(':'))),
        }],
        'force_keyframes_at_cuts': True,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return f"{output_name}.mp4"

# --- INTERFAȚA ---
url = st.text_input("Link YouTube")
col1, col2 = st.columns(2)
with col1:
    t_start = st.text_input("Start (hh:mm:ss)", "00:00:10")
with col2:
    t_end = st.text_input("Final (hh:mm:ss)", "00:00:20")

if st.button("Taie și Descarcă"):
    with st.spinner("Se procesează... durează câteva secunde."):
        try:
            file_path = download_and_cut(url, t_start, t_end, "clip_rezultat")
            st.success("Gata!")
            # Aici va apărea butonul de download după procesare
            with open(f"downloads/clip_rezultat.mp4", "rb") as file:
                st.download_button("Descarcă Clipul pe PC", file, file_name="clip_taiat.mp4")
        except Exception as e:
            st.error(f"Eroare: {e}")
