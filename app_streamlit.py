import streamlit as st
import requests, time

API = "http://127.0.0.1:8000"

st.set_page_config(page_title="Morpion 10x10", layout="wide")

def load_css(file_name):
    try:
        with open(file_name, "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except:
        pass

load_css("style.css")

# --- FONCTIONS API ---
def get_models():
    r = requests.get(f"{API}/models")
    return r.json()

def get_state():
    r = requests.get(f"{API}/state")
    return r.json()

def reset_game():
    requests.post(f"{API}/reset")

def llm_play(current_player_id):
    # Sélection du modèle basé sur le joueur actuel
    selected_model = st.session_state.model_x if current_player_id == 1 else st.session_state.model_o
    
    r = requests.post(
        f"{API}/llm-play",
        json={
            "model": selected_model,
            "temperature": 0.2
        }
    )
    return r.json()

# --- INITIALISATION ---
models = get_models()
MODEL_MAP = {m["label"]: m["id"] for m in models}
model_list = list(MODEL_MAP.keys())

if "auto" not in st.session_state: st.session_state.auto = False
if "model_x" not in st.session_state: st.session_state.model_x = MODEL_MAP[model_list[0]]
if "model_o" not in st.session_state: st.session_state.model_o = MODEL_MAP[model_list[0]]

# --- UI CONTROLES ---
st.title("🕹️ Morpion LLM: Battle")

c1, c4, c3, c2, c5, c6 = st.columns([1, 1.2, 1.2, 1, 0.8, 1.2])

with c1:
    if st.button("Relancer Jeu"):
        reset_game()
        st.session_state.auto = False
        st.rerun()

with c2:
    # On garde le label dans la session_state pour l'utiliser lors de la victoire
    st.session_state.label_x = st.selectbox("Joueur X (Bleu)", model_list, key="sb_x")
    st.session_state.model_x = MODEL_MAP[st.session_state.label_x]

with c3:
    st.session_state.label_o = st.selectbox("Joueur O (Rouge)", model_list, key="sb_o")
    st.session_state.model_o = MODEL_MAP[st.session_state.label_o]

with c4:
    if st.button("Jouer Coup IA"):
        state = get_state()
        llm_play(state["player"])
        st.rerun()

with c5:
    st.session_state.auto = st.toggle("Auto", value=st.session_state.auto)

with c6:
    delay = st.slider("Vitesse", 0.05, 1.0, 0.2, label_visibility="collapsed")

# --- ÉTAT DU JEU ---
state = get_state()
grid, player = state["grid"], state["player"]
winner, draw = state.get("winner"), state.get("draw")

# Affichage du tour actuel avec le nom du modèle
current_model_name = st.session_state.label_x if player == 1 else st.session_state.label_o
color = "#60a5fa" if player == 1 else "#f87171"

st.markdown(
    f"<p style='text-align:center; font-size:20px;'>Tour de : <b style='color:{color};'>{current_model_name}</b></p>",
    unsafe_allow_html=True
)

# --- AFFICHAGE PLATEAU ---
cells_html = ""
for r in range(10):
    for c in range(10):
        v = grid[r][c]
        cls = "cell-x" if v == 1 else "cell-o" if v == 2 else ""
        txt = "X" if v == 1 else "O" if v == 2 else ""
        cells_html += f"<div class='cell {cls}'>{txt}</div>"

st.markdown(f"<div class='board'>{cells_html}</div>", unsafe_allow_html=True)

# --- LOGIQUE DE FIN ET AUTO ---
if winner:
    st.balloons()
    # RÉCUPÉRATION DU NOM DU MODÈLE GAGNANT
    winner_name = st.session_state.label_x if winner == 1 else st.session_state.label_o
    st.success(f"🏆 Victoire de : {winner_name}")
    st.session_state.auto = False
elif draw:
    st.warning("🤝 Match Nul")
    st.session_state.auto = False
elif st.session_state.auto:
    llm_play(player)
    time.sleep(delay)
    st.rerun()