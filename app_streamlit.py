import streamlit as st
import requests, time

# --- CHARGEMENT DU STYLE EXTERNE ---
def load_css(file_name):
    with open(file_name, "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

API = "http://127.0.0.1:8000"

def get_state():
    r = requests.get(f"{API}/state", timeout=5)
    r.raise_for_status()
    return r.json()

def reset_game():
    requests.post(f"{API}/reset", timeout=5)

def llm_play():
    r = requests.post(f"{API}/llm-play", timeout=120)
    r.raise_for_status()
    return r.json()

st.set_page_config(page_title="Morpion 10x10", layout="wide")

# Appel du fichier CSS
load_css("style.css")

st.title("🕹️ Morpion LLM 10x10")

if "auto" not in st.session_state:
    st.session_state.auto = False

c1, c2, c3, c4 = st.columns([1, 1, 1, 1.5])
with c1:
    if st.button(" Relancer le jeu"):
        reset_game(); st.session_state.auto = False; st.rerun()
with c2:
    if st.button("🚀 Faire jouer l'IA"):
        res = llm_play(); st.rerun()
with c3:
    st.session_state.auto = st.toggle("Auto-Pilot", value=st.session_state.auto)
with c4:
    delay = st.slider("Vitesse", 0.05, 1.0, 0.2, 0.05, label_visibility="collapsed")

state = get_state()
grid = state["grid"]
player = state["player"]
winner = state.get("winner")
draw = state.get("draw")

st.markdown(f"<p style='text-align:center; margin:15px 0;'>Tour du Joueur : <b>{'X' if player==1 else 'O'}</b></p>", unsafe_allow_html=True)

cells_html = ""
for r in range(10):
    for c in range(10):
        val = grid[r][c]
        class_name = "cell-x" if val == 1 else "cell-o" if val == 2 else ""
        symbol_text = "X" if val == 1 else "O" if val == 2 else ""
        cells_html += f"<div class='cell {class_name}'>{symbol_text}</div>"

st.markdown(f"<div class='board'>{cells_html}</div>", unsafe_allow_html=True)

if winner:
    st.balloons(); st.success(f"🏆 Victoire du Joueur {winner} !"); st.session_state.auto = False
elif draw:
    st.warning("🤝 Match Nul !"); st.session_state.auto = False

if st.session_state.auto and not winner and not draw:
    res = llm_play(); time.sleep(delay); st.rerun()