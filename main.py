import streamlit as st
import random
import time

st.set_page_config(page_title="ADHS Hero-System", layout="centered")

# --- SESSION STATE ---
if 'mode' not in st.session_state:
    st.session_state.mode = "READY"

if 'tasks' not in st.session_state:
    st.session_state.tasks = ["🧺 Wäsche", "🧹 Saugen", "🗑️ Müll", "🍳 Küche", "🧼 Bad"]

if 'start_time' not in st.session_state:
    st.session_state.start_time = 0

if 'current_task' not in st.session_state:
    st.session_state.current_task = ""

if 'sound_flag' not in st.session_state:
    st.session_state.sound_flag = None  # "start" / "end"

# --- SOUND ---
def play_sound():
    if st.session_state.sound_flag == "start":
        st.audio("https://www.soundjay.com/buttons/sounds/button-3.mp3")
        st.session_state.sound_flag = None

    elif st.session_state.sound_flag == "end":
        st.audio("https://www.soundjay.com/human/sounds/applause-01.mp3")
        st.session_state.sound_flag = None

# --- TIMER ---
def get_remaining(start, duration):
    return max(0, duration - (time.time() - start))

def fmt(sec):
    return f"{int(sec//60):02d}:{int(sec%60):02d}"

# --- UI ---
st.title("⚡ ADHS Hero-System")

play_sound()

# --- TASKS ---
with st.expander("📋 Aufgaben-Pool"):
    new = st.text_input("Neue Mission")

    if st.button("Hinzufügen") and new:
        st.session_state.tasks.append(new)
        st.rerun()

    for i, t in enumerate(st.session_state.tasks):
        c1, c2 = st.columns([4,1])
        c1.write(t)
        if c2.button("X", key=i):
            st.session_state.tasks.pop(i)
            st.rerun()

# --- READY ---
if st.session_state.mode == "READY":
    if st.button("🚀 START"):
        if not st.session_state.tasks:
            st.error("Keine Aufgaben")
        else:
            st.session_state.current_task = random.choice(st.session_state.tasks)
            st.session_state.start_time = time.time()
            st.session_state.mode = "WORKING"
            st.session_state.sound_flag = "start"
            st.rerun()

# --- WORKING ---
elif st.session_state.mode == "WORKING":
    st.info(f"MISSION: {st.session_state.current_task}")

    remaining = get_remaining(st.session_state.start_time, 15*60)

    st.metric("Zeit", fmt(remaining))
    st.progress(1 - remaining/(15*60))

    if st.button("FERTIG") or remaining <= 0:
        st.session_state.mode = "PAUSE"
        st.session_state.start_time = time.time()
        st.session_state.sound_flag = "end"
        st.balloons()
        st.rerun()

    # kontrollierter refresh
    time.sleep(1)
    st.rerun()

# --- PAUSE ---
elif st.session_state.mode == "PAUSE":
    st.warning("Pause")

    remaining = get_remaining(st.session_state.start_time, 10*60)

    st.metric("Pause", fmt(remaining))
    st.progress(1 - remaining/(10*60))

    if st.button("Weiter") or remaining <= 0:
        st.session_state.mode = "READY"
        st.session_state.sound_flag = "start"
        st.rerun()

    time.sleep(1)
    st.rerun()
