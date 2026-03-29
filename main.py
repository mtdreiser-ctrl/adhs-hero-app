import streamlit as st
import random
import time

st.set_page_config(page_title="ADHS Hero-System", layout="centered")

# --- SOUND ---
def play_audio(url):
    st.audio(url, autoplay=True)

START_SOUND = "https://www.soundjay.com/buttons/sounds/button-3.mp3"
END_SOUND = "https://www.soundjay.com/human/sounds/applause-01.mp3"

# --- SESSION STATE INIT ---
if 'mode' not in st.session_state:
    st.session_state.mode = "READY"

if 'tasks' not in st.session_state:
    st.session_state.tasks = ["🧺 Wäsche", "🧹 Saugen", "🗑️ Müll", "🍳 Küche", "🧼 Bad"]

if 'start_time' not in st.session_state:
    st.session_state.start_time = 0

if 'current_task' not in st.session_state:
    st.session_state.current_task = ""

# --- UI ---
st.title("⚡ ADHS Hero-System")

# --- AUFGABEN ---
with st.expander("📋 Aufgaben-Pool bearbeiten"):
    c1, c2 = st.columns([3, 1])
    
    with c1:
        new_task = st.text_input("Neue Mission:", key="input_new")
    
    with c2:
        if st.button("Hinzufügen") and new_task:
            st.session_state.tasks.append(new_task)
            st.rerun()

    st.write("---")

    for i, task in enumerate(st.session_state.tasks):
        cols = st.columns([4, 1])
        cols[0].write(f"• {task}")
        if cols[1].button("🗑️", key=f"del_{i}"):
            st.session_state.tasks.pop(i)
            st.rerun()

# --- TIMER FUNKTION ---
def get_remaining(start, duration_sec):
    elapsed = time.time() - start
    return max(0, duration_sec - elapsed)

def format_time(sec):
    return f"{int(sec//60):02d}:{int(sec%60):02d}"

# --- MODES ---

# READY
if st.session_state.mode == "READY":
    if st.button("🚀 MISSION STARTEN"):
        if st.session_state.tasks:
            st.session_state.current_task = random.choice(st.session_state.tasks)
            st.session_state.start_time = time.time()
            st.session_state.mode = "WORKING"
            play_audio(START_SOUND)
            st.rerun()
        else:
            st.error("Pool ist leer!")

# WORKING
elif st.session_state.mode == "WORKING":
    st.info(f"MISSION: {st.session_state.current_task}")

    remaining = get_remaining(st.session_state.start_time, 15 * 60)

    st.metric("⏱️ Fokuszeit", format_time(remaining))

    progress = 1 - (remaining / (15 * 60))
    st.progress(progress)

    if st.button("✅ FERTIG!") or remaining <= 0:
        play_audio(END_SOUND)
        st.balloons()
        st.session_state.mode = "PAUSE"
        st.session_state.start_time = time.time()
        st.rerun()

    # sanfter Auto-Refresh
    st.markdown(
        "<meta http-equiv='refresh' content='1'>",
        unsafe_allow_html=True
    )

# PAUSE
elif st.session_state.mode == "PAUSE":
    st.warning("⏸️ PAUSE")

    remaining = get_remaining(st.session_state.start_time, 10 * 60)

    st.metric("⏱️ Rest", format_time(remaining))

    progress = 1 - (remaining / (10 * 60))
    st.progress(progress)

    if remaining <= 0 or st.button("🔄 Nächste Runde"):
        play_audio(START_SOUND)
        st.session_state.mode = "READY"
        st.rerun()

    st.markdown(
        "<meta http-equiv='refresh' content='1'>",
        unsafe_allow_html=True
    )
