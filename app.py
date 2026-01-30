import streamlit as st
import yt_dlp
import os

st.set_page_config(page_title="Clipper Direct", page_icon="✂️")
st.title("✂️ Metoda Alternativă (Anti-Blocaj)")

if not os.path.exists("downloads"):
    os.makedirs("downloads")

def download_with_fallback(url, start, end, index):
    output_name = f"downloads/clip_{index}.mp4"
    
    # Folosim cele mai "blânde" setări posibile
    ydl_opts = {
        'format': 'mp4/best', # Forțăm MP4 direct pentru a evita procesarea grea
        'outtmpl': output_name,
        'quiet': True,
        'download_sections': [{'start_time': start, 'end_time': end}],
        'force_keyframes_at_cuts': True,
        # Adăugăm un user agent de mobil (uneori YouTube e mai blând cu ele)
        'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1',
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return output_name

url = st.text_input("Link YouTube")
seg = st.number_input("Secunde per clip", 5, 600, 15)
num = st.number_input("Câte segmente?", 1, 5, 1)

if st.button("Încearcă din nou"):
    if url:
        for i in range(num):
            start = i * seg
            end = start + seg
            try:
                with st.spinner(f"Încercăm segmentul {i+1}..."):
                    file_path = download_with_fallback(url, start, end, i+1)
                    with open(file_path, "rb") as f:
                        st.download_button(f"📥 Descarcă Clip {i+1}", f, file_name=f"clip_{i+1}.mp4")
            except Exception as e:
                st.error(f"YouTube încă blochează serverul. Eroare: {e}")
                st.warning("⚠️ Dacă nici asta nu merge, înseamnă că Streamlit este blocat total pe IP. Soluția ar fi să rulezi codul local sau pe Replit.")
