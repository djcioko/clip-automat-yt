import streamlit as st
import os
import subprocess

st.set_page_config(page_title="Video Cutter Local", page_icon="✂️")
st.title("✂️ Tăiere Video (Fără YouTube)")

# Folder pentru procesare
if not os.path.exists("temp"):
    os.makedirs("temp")

# 1. Încărcare fișier
uploaded_file = st.file_uploader("Încarcă un fișier MP4", type=["mp4", "mov", "avi"])

if uploaded_file is not None:
    # Salvăm fișierul original temporar
    input_path = os.path.join("temp", "input_video.mp4")
    with open(input_path, "wb") as f:
        f.write(uploaded_file.read())
    
    st.success("Fișier încărcat cu succes!")
    st.video(input_path) # Prevualizare video

    # 2. Setări tăiere
    st.subheader("Setări Tăiere")
    col1, col2 = st.columns(2)
    with col1:
        start_t = st.text_input("Start (secunde sau hh:mm:ss)", "0")
    with col2:
        duration_t = st.text_input("Durată clip (secunde)", "15")

    if st.button("Taie Video"):
        output_path = os.path.join("temp", "clip_taiat.mp4")
        
        # Folosim FFmpeg (instalat prin packages.txt) pentru tăiere rapidă
        # Comanda: ffmpeg -ss [start] -i [input] -t [duration] -c copy [output]
        command = [
            "ffmpeg", "-y",
            "-ss", str(start_t),
            "-i", input_path,
            "-t", str(duration_t),
            "-c", "copy",
            output_path
        ]
        
        try:
            with st.spinner("Se taie..."):
                subprocess.run(command, check=True)
                
            with open(output_path, "rb") as file:
                st.download_button(
                    label="📥 Descarcă Clipul Tăiat",
                    data=file,
                    file_name="clip_nou.mp4",
                    mime="video/mp4"
                )
        except Exception as e:
            st.error(f"Eroare la tăiere: {e}")

# Curățare istoric (opțional)
if st.sidebar.button("Șterge fișierele temporare"):
    for f in os.listdir("temp"):
        os.remove(os.path.join("temp", f))
    st.rerun()
