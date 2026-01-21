# app_streamlit.py
import streamlit as st
import requests

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

col1, col2 = st.columns(2)
with col1:
    if st.button("Reset"):
        reset_game()
with col2:
    if st.button("Faire jouer le LLM"):
        res = llm_play()
        if "error" in res:
            st.error(res["error"])
            st.write(res.get("details", ""))
            st.write(res.get("texte_llm", ""))
        else:
            st.success(f"LLM a joué: {res['coup']}")
            st.write("Réponse LLM:", res["texte_llm"])
            if res.get("winner"):
                st.warning(f"Winner: {res['winner']} (1=X, 2=O)")
            if res.get("draw"):
                st.warning("Match nul")

state = get_state()
grid = state["grid"]
player = state["player"]

st.write(f"Joueur courant: {player}  (1=X, 2=O)")

symbol_map = {0: "", 1: "X", 2: "O"}
cells = []
for r in range(10):
    for c in range(10):
        cells.append(f"<div class='cell'>{symbol_map.get(grid[r][c], '')}</div>")

html = f"""
<style>
.board {{
  display: grid;
  grid-template-columns: repeat(10, 42px);
  gap: 6px;
  justify-content: center;
  margin-top: 16px;
}}
.cell {{
  width: 42px;
  height: 42px;
  border: 1px solid #bbb;
  border-radius: 10px;
  display: grid;
  align-items: center;
  justify-content: center;
  font-size: 22px;
  font-weight: 800;
}}
</style>
<div class="board">
  {''.join(cells)}
</div>
"""
st.markdown(html, unsafe_allow_html=True)
