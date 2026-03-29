import streamlit as st
import random
import time

st.set_page_config(page_title="ADHS Hero-System", layout="centered")

# --- SOUND FUNKTION (Direkt-Injection) ---
def play_sound(url):
    st.components.v1.html(
        f"""
        <audio autoplay style="display:none">
            <source src="{url}" type="audio/mpeg">
        </audio>
        """,
        height=0,
    )

START_SOUND = "https://www.soundjay.com/buttons/sounds/button-3.mp3"
WIN_SOUND = "https://www.soundjay.com/human/sounds/applause-01.mp3"

# --- DESIGN ---
st.markdown("""
<style>
    .main { background-color: #0E1117; color: #FFFFFF; }
    .stButton>button { height: 70px; border-radius: 15px; font-weight: bold; font-size: 20px !important; width: 100%; }
    .pause-box { background-color: #262730; padding: 20px; border-radius: 15px; border: 2px solid #00D1FF; text-align: center; }
</style>
""", unsafe_allow_html=True)

# --- DATEN-VERWALTUNG ---
if 'mode' not in st.session_state: st.session_state.mode = "READY"
if 'custom_tasks' not in st.session_state: st.session_state.custom_tasks = []

default_tasks = ["Wäsche", "Saugen", "Müll", "Küche", "Bad"]

st.title("⚡ ADHS Hero-System")

# --- NEU: AUFGABEN-MANAGER ---
with st.expander("➕ Eigene Aufgaben hinzufügen"):
    new_task = st.text_input("Was steht an?")
    if st.button("Hinzufügen") and new_task:
        st.session_state.custom_tasks.append(new_task)
        st.success(f"'{new_task}' ist im Pool!")

# --- LOGIK: READY MODE ---
if st.session_state.mode == "READY":
    all_tasks = default_tasks + st.session_state.custom_tasks
    st.write(f"Verfügbare Aufgaben: {len(all_tasks)}")
    
    if st.button("🚀 MISSION STARTEN"):
        st.session_state.current_task = random.choice(all_tasks)
        st.session_state.mode = "WORKING"
        st.session_state.start_time = time.time()
        play_sound(START_SOUND)
        st.rerun()

# --- LOGIK: WORKING MODE ---
elif st.session_state.mode == "WORKING":
    st.info(f"AKTUELLE MISSION: {st.session_state.current_task}")
    
    elapsed = time.time() - st.session_state.start_time
    remaining = max(0, 15 * 60 - elapsed)
    
    st.progress(min(1.0, elapsed / (15 * 60)))
    st.write(f"⏱️ Noch {int(remaining//60):02d}:{int(remaining%60):02d}")

    if st.button("✅ ERLEDIGT!") or remaining <= 0:
        play_sound(WIN_SOUND)
        st.balloons()
        st.session_state.mode = "PAUSE"
        st.session_state.start_time = time.time()
        st.rerun()
    
    time.sleep(1)
    st.rerun()

# --- LOGIK: PAUSE MODE ---
elif st.session_state.mode == "PAUSE":
    st.markdown('<div class="pause-box"><h2>⏸️ PAUSEN-MODUS</h2><p>Kurz durchatmen!</p></div>', unsafe_allow_html=True)
    
    elapsed = time.time() - st.session_state.start_time
    remaining_pause = max(0, 10 * 60 - elapsed)
    st.warning(f"Noch {int(remaining_pause//60):02d}:{int(remaining_pause%60):02d} Minuten.")
    
    if remaining_pause <= 0 or st.button("🔄 Weiter"):
        st.session_state.mode = "READY"
        st.rerun()
    
    time.sleep(1)
    st.rerun()
