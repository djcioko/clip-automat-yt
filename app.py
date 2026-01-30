import streamlit as st
import yt_dlp
import os

st.set_page_config(page_title="YouTube Clipper Simple", page_icon="✂️")
st.title("✂️ YouTube Clipper - Descărcare Directă")

# Folder pentru salvări temporare
if not os.path.exists("downloads"):
    os.makedirs("downloads")

def download_single_clip(url, start_time, end_time, index):
    output_name = f"downloads/clip_{index}.mp4"
    
    ydl_opts = {
        'format': 'best',
        'outtmpl': output_name,
        'quiet': True,
        'nocheckcertificate': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'download_sections': [{
            'start_time': start_time,
            'end_time': end_time,
        }],
        'force_keyframes_at_cuts': True,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return output_name

# --- INTERFAȚĂ ---
url = st.text_input("Link YouTube")
seg = st.number_input("Lungime segment (secunde)", 5, 600, 15)
num = st.number_input("Câte segmente vrei?", 1, 10, 1)

if st.button("Taie Clipurile"):
    if url:
        for i in range(num):
            start = i * seg
            end = start + seg
            try:
                with st.spinner(f"Se procesează segmentul {i+1}..."):
                    file_path = download_single_clip(url, start, end, i+1)
                    with open(file_path, "rb") as f:
                        st.download_button(f"📥 Descarcă Clip {i+1} ({start}s-{end}s)", f, file_name=f"clip_{i+1}.mp4")
            except Exception as e:
                st.error(f"Eroare la clipul {i+1}: {e}")
    else:
        st.warning("Introdu un link mai întâi!")
