import streamlit as st
import random
import time
import base64

st.set_page_config(page_title="ADHS Pro-Pilot", layout="centered")

# --- AUDIO FUNKTION (Vibe-Check) ---
def play_sound(url):
    sound_html = f"""
        <audio autoplay>
            <source src="{url}" type="audio/mpeg">
        </audio>
    """
    st.markdown(sound_html, unsafe_allow_html=True)

# Sound-URLs (Public Assets)
START_SOUND = "https://www.soundjay.com/buttons/sounds/button-3.mp3"
WIN_SOUND = "https://www.soundjay.com/human/sounds/applause-01.mp3"

# --- CSS & DESIGN ---
st.markdown("""
<style>
    .main { background-color: #0E1117; color: #FFFFFF; }
    .stButton>button { height: 70px; border-radius: 15px; font-weight: bold; font-size: 20px !important; }
    .pause-box { background-color: #262730; padding: 20px; border-radius: 15px; border: 2px solid #00D1FF; text-align: center; }
</style>
""", unsafe_allow_html=True)

# --- STATE MANAGEMENT ---
if 'mode' not in st.session_state: st.session_state.mode = "READY"
if 'start_time' not in st.session_state: st.session_state.start_time = 0

tasks = {
    "High Energy": ["Wäsche", "Saugen", "Müll", "Küche", "Bad"],
    "Low Battery": ["Socken sortieren", "Mails löschen", "Post", "Fotos", "Planen"]
}

st.title("⚡ ADHS Hero-System")

# --- LOGIK: READY MODE ---
if st.session_state.mode == "READY":
    low_battery = st.toggle("Low Battery Mode 🪫")
    if st.button("🚀 MISSION STARTEN"):
        pool = tasks["Low Battery"] if low_battery else tasks["High Energy"]
        st.session_state.current_task = random.choice(pool)
        st.session_state.mode = "WORKING"
        st.session_state.start_time = time.time()
        play_sound(START_SOUND)
        st.rerun()

# --- LOGIK: WORKING MODE (15-20 Min) ---
elif st.session_state.mode == "WORKING":
    st.info(f"AKTUELLE MISSION: {st.session_state.current_task}")
    
    elapsed = time.time() - st.session_state.start_time
    remaining = max(0, 15 * 60 - elapsed)
    
    st.progress(min(1.0, elapsed / (15 * 60)))
    
    timer_placeholder = st.empty()
    timer_placeholder.write(f"⏱️ Noch {int(remaining//60):02d}:{int(remaining%60):02d}")

    if remaining <= 0:
        play_sound(WIN_SOUND)
        st.balloons()
        st.session_state.mode = "PAUSE"
        st.session_state.start_time = time.time()
        st.rerun()
    else:
        if st.button("✅ ERLEDIGT!"):
            play_sound(WIN_SOUND)
            st.balloons()
            st.session_state.mode = "PAUSE"
            st.session_state.start_time = time.time()
            st.rerun()
        time.sleep(1)
        st.rerun()

# --- LOGIK: PAUSE MODE (10 Min) ---
elif st.session_state.mode == "PAUSE":
    st.markdown('<div class="pause-box"><h2>⏸️ PAUSEN-MODUS</h2><p>Zeit zum Regenerieren. Keine neue Aufgabe möglich!</p></div>', unsafe_allow_html=True)
    
    elapsed = time.time() - st.session_state.start_time
    remaining_pause = max(0, 10 * 60 - elapsed)
    
    timer_placeholder = st.empty()
    timer_placeholder.warning(f"Noch {int(remaining_pause//60):02d}:{int(remaining_pause%60):02d} Minuten ausruhen.")
    
    if remaining_pause <= 0:
        if st.button("🔄 Wieder einsatzbereit?"):
            st.session_state.mode = "READY"
            st.rerun()
    else:
        time.sleep(1)
        st.rerun()
