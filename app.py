import streamlit as st
import yt_dlp
import os
import zipfile
import shutil

st.set_page_config(page_title="YouTube Batch Clipper", page_icon="✂️")
st.title("✂️ YouTube Automatic Batch Clipper")

# Curățăm folderele vechi la pornire
if os.path.exists("temp_clips"):
    shutil.rmtree("temp_clips")
os.makedirs("temp_clips")

def download_batch_clips(url, interval_sec, total_clips):
    zip_path = "clips_arhiva.zip"
    
    with yt_dlp.YoutubeDL({'format': 'bestvideo+bestaudio/best', 'quiet': True}) as ydl:
        info = ydl.extract_info(url, download=False)
        duration = info.get('duration', 0)

    for i in range(total_clips):
        start_time = i * interval_sec
        end_time = start_time + interval_sec
        
        if start_time >= duration:
            break
            
        output_name = f"temp_clips/clip_{i+1}_{start_time}_{end_time}.mp4"
        
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': output_name,
            'download_sections': [{
                'start_time': start_time,
                'end_time': end_time,
            }],
            'force_keyframes_at_cuts': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            st.write(f"✅ Procesat clipul {i+1} ({start_time}s - {end_time}s)")

    # Creăm arhiva ZIP
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for root, dirs, files in os.walk("temp_clips"):
            for file in files:
                zipf.write(os.path.join(root, file), file)
    
    return zip_path

# --- INTERFAȚA ---
url = st.text_input("Link YouTube")
col1, col2 = st.columns(2)

with col1:
    segment_sec = st.number_input("Lungime clip (secunde)", min_value=5, max_value=600, value=15)
with col2:
    num_clips = st.number_input("Câte clipuri să tai?", min_value=1, max_value=20, value=5)

if st.button("Începe Tăierea Batch (ZIP)"):
    if url:
        with st.spinner("Se descarcă și se taie..."):
            try:
                zip_file = download_batch_clips(url, segment_sec, num_clips)
                with open(zip_file, "rb") as f:
                    st.download_button("📥 Descarcă Toate Clipurile (ZIP)", f, file_name="clipuri_youtube.zip")
                st.success(f"Gata! Am tăiat {num_clips} clipuri.")
            except Exception as e:
                st.error(f"Eroare: {e}")
    else:
        st.warning("Te rog introdu un link!")
