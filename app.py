import streamlit as st
import os
import subprocess
import zipfile
import shutil

st.set_page_config(page_title="Multi-Clipper Local", page_icon="✂️")
st.title("✂️ Tăiere Automată în Masă (Batch)")

# Creăm folderele necesare
TEMP_DIR = "temp_input"
OUTPUT_DIR = "clips_output"

for folder in [TEMP_DIR, OUTPUT_DIR]:
    if not os.path.exists(folder):
        os.makedirs(folder)

# Funcție pentru a obține durata video folosind ffprobe
def get_video_duration(file_path):
    cmd = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", file_path
    ]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return float(result.stdout)

# 1. Încărcare fișier
uploaded_file = st.file_uploader("Încarcă videoclipul de o oră (MP4)", type=["mp4"])

if uploaded_file is not None:
    input_path = os.path.join(TEMP_DIR, "video_sursa.mp4")
    with open(input_path, "wb") as f:
        f.write(uploaded_file.read())
    
    st.success("✅ Videoclip încărcat!")
    
    # 2. Setări Batch
    st.subheader("Setări tăiere automată")
    seg_length = st.number_input("Lungime segment (secunde)", min_value=1, value=15)
    max_clips = st.number_input("Număr maxim de clipuri de generat", min_value=1, value=20)

    if st.button("Începe Tăierea Automată"):
        try:
            duration = get_video_duration(input_path)
            st.info(f"Durata totală detectată: {duration:.2f} secunde.")
            
            # Curățăm folderul de output de tăieri vechi
            shutil.rmtree(OUTPUT_DIR)
            os.makedirs(OUTPUT_DIR)
            
            progress_bar = st.progress(0)
            
            for i in range(max_clips):
                start_time = i * seg_length
                if start_time >= duration:
                    break
                
                output_filename = f"clip_{i+1}.mp4"
                output_path = os.path.join(OUTPUT_DIR, output_filename)
                
                # Comanda FFmpeg pentru tăiere ultra-rapidă fără re-encodare
                command = [
                    "ffmpeg", "-y", "-ss", str(start_time), "-t", str(seg_length),
                    "-i", input_path, "-c", "copy", output_path
                ]
                subprocess.run(command, capture_output=True)
                
                # Update progres
                progress = (i + 1) / max_clips
                progress_bar.progress(min(progress, 1.0))

            # 3. Împachetare în ZIP pentru descărcare rapidă
            zip_name = "toate_clipurile.zip"
            with zipfile.ZipFile(zip_name, 'w') as zipf:
                for root, dirs, files in os.walk(OUTPUT_DIR):
                    for file in files:
                        zipf.write(os.path.join(root, file), file)
            
            st.success(f"Gata! Am tăiat {i+1} clipuri.")
            with open(zip_name, "rb") as f:
                st.download_button("📥 DESCARCĂ TOATE CLIPURILE (ZIP)", f, file_name=zip_name)
                
        except Exception as e:
            st.error(f"Eroare: {e}. Asigură-te că ai 'ffmpeg' în packages.txt.")

# Buton de curățare
if st.sidebar.button("Șterge tot și resetează"):
    shutil.rmtree(TEMP_DIR, ignore_errors=True)
    shutil.rmtree(OUTPUT_DIR, ignore_errors=True)
    if os.path.exists("toate_clipurile.zip"): os.remove("toate_clipurile.zip")
    st.rerun()
