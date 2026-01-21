# app_streamlit.py
import streamlit as st
import requests, time

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
st.title("Morpion 10x10 - LLM")

if "auto" not in st.session_state:
    st.session_state.auto = False

c1, c2, c3 = st.columns(3)
with c1:
    if st.button("Reset"):
        reset_game()
        st.session_state.auto = False
with c2:
    st.session_state.auto = st.toggle("Auto Play", value=st.session_state.auto)
with c3:
    delay = st.slider("Delay (sec)", 0.5, 3.0, 1.2, 0.1)

state = get_state()
grid = state["grid"]
player = state["player"]
winner = state.get("winner")
draw = state.get("draw")

st.write(f"Joueur: {player}  (1=X, 2=O)")

symbol = {0: "", 1: "X", 2: "O"}
cells = [f"<div class='cell'>{symbol.get(grid[r][c],'')}</div>" for r in range(10) for c in range(10)]
st.markdown(f"""
<style>
.board {{display:grid;grid-template-columns:repeat(10,42px);gap:6px;justify-content:center;margin-top:12px;}}
.cell {{width:42px;height:42px;border:1px solid #bbb;border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:22px;font-weight:800;}}
</style>
<div class="board">{''.join(cells)}</div>
""", unsafe_allow_html=True)

if st.button("Faire jouer le LLM"):
    res = llm_play()
    st.info(res.get("note", ""))
    st.write("Coup:", res.get("coup"))
    with st.expander("LLM reasoning (optional)"):
        st.write(res.get("texte_llm", ""))

    st.rerun() 



if winner:
    st.success(f"Winner: {winner} (1=X, 2=O)")
    st.session_state.auto = False
elif draw:
    st.warning("Draw")
    st.session_state.auto = False

if st.session_state.auto and not winner and not draw:
    res = llm_play()
    time.sleep(delay)
    st.rerun()
