import streamlit as st
import random
import time

# --- SEITEN-KONFIGURATION ---
st.set_page_config(page_title="ADHS Hero-System", layout="centered")

# --- AUDIO FUNKTION (Web-Standard) ---
def play_sound(url):
    sound_html = f"""
        <audio autoplay>
            <source src="{url}" type="audio/mpeg">
        </audio>
    """
    st.markdown(sound_html, unsafe_allow_html=True)

# Sound-URLs
START_SOUND = "https://www.soundjay.com/buttons/sounds/button-3.mp3"
WIN_SOUND = "https://www.soundjay.com/human/sounds/applause-01.mp3"

# --- DESIGN (CSS) ---
st.markdown("""
<style>
    .main { background-color: #0E1117; color: #FFFFFF; }
    .stButton>button { 
        height: 80px; width: 100%; border-radius: 20px; 
        font-weight: bold; font-size: 22px !important;
        background: linear-gradient(45deg, #FF4B4B, #FF914D);
        color: white; border: none;
    }
    .task-card { 
        background-color: #1E1E1E; padding: 25px; border-radius: 20px; 
        border: 2px solid #FF4B4B; text-align: center; margin: 20px 0;
    }
    .pause-box { 
        background-color: #1E1E1E; padding: 25px; border-radius: 20px; 
        border: 2px solid #00D1FF; text-align: center; margin: 20px 0;
    }
</style>
""", unsafe_allow_html=True)

# --- INITIALISIERUNG (SYSTEM-START) ---
if 'mode' not in st.session_state:
    st.session_state.mode = "READY"
if 'current_task' not in st.session_state:
    st.session_state.current_task = ""
if 'start_time' not in st.session_state:
    st.session_state.start_time = 0

# Aufgaben-Datenbank
tasks = {
    "High Energy": ["🧺 Wäsche machen", "🧹 Saugen", "🗑️ Müll rausbringen", "🍳 Küche aufräumen", "🧼 Bad putzen"],
    "Low Battery": ["🧦 Socken sortieren", "📧 Mails löschen", "📝 Einkaufsliste schreiben", "📁 Post sortieren", "📱 Fotos aussortieren"]
}

st.title("⚡ ADHS Hero-System")

# --- MODUS: BEREIT (READY) ---
if st.session_state.mode == "READY":
    st.write("Wähle dein Energielevel für die nächste Mission:")
    low_battery = st.toggle("Low Battery Mode 🪫 (Sitzen/Ruhig)")
    
    if st.button("🚀 NÄCHSTE MISSION STARTEN"):
        pool = tasks["Low Battery"] if low_battery else tasks["High Energy"]
        st.session_state.current_task = random.choice(pool)
        st.session_state.start_time = time.time()
        st.session_state.mode = "WORKING"
        play_sound(START_SOUND)
        st.rerun()

# --- MODUS: ARBEIT (WORKING) ---
elif st.session_state.mode == "WORKING":
    st.markdown(f"""
    <div class="task-card">
        <p style="color: #888;">DEINE MISSION:</p>
        <h2>{st.session_state.current_task}</h2>
    </div>
    """, unsafe_allow_html=True)
    
    elapsed = time.time() - st.session_state.start_time
    duration = 15 * 60 # 15 Minuten
    remaining = max(0, duration - elapsed)
    
    st.progress(min(1.0, elapsed / duration))
    st.write(f"⏱️ Fokus-Timer: {int(remaining//60):02d}:{int(remaining%60):02d}")

    if st.button("✅ ICH BIN FERTIG!") or remaining <= 0:
        play_sound(WIN_SOUND)
        st.balloons()
        st.session_state.mode = "PAUSE"
        st.session_state.start_time = time.time() # Reset für Pause-Timer
        st.rerun()

# --- MODUS: PAUSE (PAUSE) ---
elif st.session_state.mode == "PAUSE":
    st.markdown("""
    <div class="pause-box">
        <h2 style="color: #00D1FF;">⏸️ PAUSEN-MODUS</h2>
        <p>Gönn deinem Kopf 10 Minuten Ruhe. Trink ein Glas Wasser!</p>
    </div>
    """, unsafe_allow_html=True)
    
    elapsed = time.time() - st.session_state.start_time
    pause_duration = 10 * 60 # 10 Minuten
    remaining_pause = max(0, pause_duration - elapsed)
    
    st.warning(f"Pause läuft: Noch {int(remaining_pause//60):02d}:{int(remaining_pause%60):02d} Minuten.")
    
    if remaining_pause <= 0:
        if st.button("🔄 Wieder einsatzbereit?"):
            st.session_state.mode = "READY"
            st.rerun()
    else:
        # Kleiner Button zum Pausen-Überspringen (nur für Notfälle)
        if st.button("⏩ Pause abkürzen"):
            st.session_state.mode = "READY"
            st.rerun()
