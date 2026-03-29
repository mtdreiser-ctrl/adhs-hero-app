import streamlit as st
import random
import time

# --- SEITEN-SETUP ---
st.set_page_config(page_title="ADHS Hero-System", layout="centered")

# --- SOUND-ENGINE (Triggert immer) ---
def play_audio(url):
    st.components.v1.html(
        f"""<audio autoplay><source src="{url}" type="audio/mpeg"></audio>""",
        height=0,
    )

START_SOUND = "https://www.soundjay.com/buttons/sounds/button-3.mp3"
END_SOUND = "https://www.soundjay.com/human/sounds/applause-01.mp3"

# --- SYSTEM-SPEICHER ---
if 'mode' not in st.session_state: st.session_state.mode = "READY"
if 'tasks' not in st.session_state: 
    st.session_state.tasks = ["🧺 Wäsche", "🧹 Saugen", "🗑️ Müll", "🍳 Küche", "🧼 Bad"]
if 'start_time' not in st.session_state: st.session_state.start_time = 0

st.title("⚡ ADHS Hero-System")

# --- AUFGABEN-VERWALTUNG (Löschen & Hinzufügen) ---
with st.expander("📋 Aufgaben-Pool bearbeiten"):
    # Neue Aufgabe hinzufügen
    c1, c2 = st.columns([3, 1])
    with c1:
        new_t = st.text_input("Neue Mission eingeben:", key="input_new")
    with c2:
        if st.button("Hinzufügen") and new_t:
            st.session_state.tasks.append(new_t)
            st.rerun()
    
    st.write("---")
    # Liste der aktuellen Aufgaben mit Lösch-Option
    for i, t in enumerate(st.session_state.tasks):
        cols = st.columns([4, 1])
        cols[0].write(f"• {t}")
        if cols[1].button("🗑️", key=f"del_{i}"):
            st.session_state.tasks.pop(i)
            st.rerun()

# --- LOGIK: BEREIT ---
if st.session_state.mode == "READY":
    st.write(f"Aktuell {len(st.session_state.tasks)} Aufgaben im Pool.")
    if st.button("🚀 MISSION STARTEN"):
        if len(st.session_state.tasks) > 0:
            st.session_state.current_task = random.choice(st.session_state.tasks)
            st.session_state.mode = "WORKING"
            st.session_state.start_time = time.time()
            play_audio(START_SOUND)
            st.rerun()
        else:
            st.error("Bitte zuerst eine Aufgabe hinzufügen!")

# --- LOGIK: ARBEIT (15 Min) ---
elif st.session_state.mode == "WORKING":
    st.info(f"AKTUELLE MISSION: {st.session_state.current_task}")
    
    elapsed = time.time() - st.session_state.start_time
    rem = max(0, 15 * 60 - elapsed)
    
    st.progress(min(1.0, elapsed / (15 * 60)))
    st.write(f"⏱️ Fokus: {int(rem//60):02d}:{int(rem%60):02d}")

    if st.button("✅ ERLEDIGT!") or rem <= 0:
        play_audio(END_SOUND)
        st.balloons()
        st.session_state.mode = "PAUSE"
        st.session_state.start_time = time.time()
        st.rerun()
    
    time.sleep(1)
    st.rerun()

# --- LOGIK: PAUSE (10 Min) ---
elif st.session_state.mode == "PAUSE":
    st.warning("⏸️ PAUSEN-MODUS")
    
    elapsed = time.time() - st.session_state.start_time
    rem_p = max(0, 10 * 60 - elapsed)
    st.write(f"⏱️ Pause: {int(rem_p//60):02d}:{int(rem_p%60):02d}")
    
    if rem_p <= 0 or st.button("🔄 Nächste Runde?"):
        play_audio(START_SOUND) # Sound auch bei neuem Start nach Pause
        st.session_state.mode = "READY"
        st.rerun()
    
    time.sleep(1)
    st.rerun()
