import streamlit as st
import json
import os

# Titlul aplicației
st.set_page_config(page_title="YouTube Auto Clipper", page_icon="✂️")
st.title("✂️ YouTube Automatic Clipper")

DB_FILE = "database.json"

# Funcție pentru a încărca datele salvate
def load_data():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return []

# Funcție pentru a salva datele
def save_data(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

# Inițializăm datele în "session_state" (memoria curentă a paginii)
if "clips" not in st.session_state:
    st.session_state.clips = load_data()

# --- INTERFAȚA ---
with st.sidebar:
    st.header("Adaugă Clip Nou")
    url = st.text_input("Link YouTube")
    t_start = st.text_input("Start (ex: 00:01:10)")
    t_end = st.text_input("Final (ex: 00:01:40)")
    
    if st.button("Salvează în listă"):
        if url and t_start and t_end:
            new_clip = {"url": url, "start": t_start, "end": t_end, "status": "Pending"}
            st.session_state.clips.append(new_clip)
            save_data(st.session_state.clips)
            st.success("Salvat!")
        else:
            st.error("Completează toate câmpurile!")

# --- AFIȘARE CLIPURI SALVATE ---
st.subheader("📋 Clipuri de procesat")
if st.session_state.clips:
    for i, clip in enumerate(st.session_state.clips):
        with st.expander(f"Clip #{i+1} - {clip['url'][:30]}..."):
            st.write(f"**URL:** {clip['url']}")
            st.write(f"**Interval:** {clip['start']} -> {clip['end']}")
            if st.button(f"Procesează Clip #{i+1}", key=f"btn_{i}"):
                st.info("Aici vom integra logica de tăiere cu yt-dlp...")
else:
    st.info("Nu ai niciun clip salvat încă.")

if st.button("Șterge tot istoricul"):
    st.session_state.clips = []
    save_data([])
    st.rerun()