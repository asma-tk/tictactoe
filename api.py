# api.py
from fastapi import FastAPI
import requests, re
from game import Game
from prompt import build_prompt

app = FastAPI()
game = Game(size=10)

def call_mistral(prompt: str) -> str:
    r = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "mistral", "prompt": prompt, "stream": False},
        timeout=120,
    )
    r.raise_for_status()
    return r.json().get("response", "")

def parse_move(txt: str):
    m = re.search(r"Coup\s*:\s*(\d+)\s*,\s*(\d+)", txt, re.IGNORECASE)
    if m:
        return int(m.group(1)), int(m.group(2))

    m = re.search(r"(\d+)\s*,\s*(\d+)", txt)
    if m:
        return int(m.group(1)), int(m.group(2))

    nums = re.findall(r"\d+", txt)
    if len(nums) >= 2:
        return int(nums[0]), int(nums[1])

    raise ValueError("No move found")

@app.get("/state")
def state():
    return {"grid": game.grid, "player": game.player, "winner": game.winner(), "draw": game.draw()}

@app.post("/reset")
def reset():
    game.reset()
    return {"ok": True}

@app.post("/llm-play")
def llm_play():
    w = game.winner()
    d = game.draw()
    if w or d:
        return {"grid": game.grid, "player": game.player, "winner": w, "draw": d, "note": "game_over"}

    prompt = build_prompt(game.grid, game.player)
    txt = call_mistral(prompt)

    note = "ok"
    try:
        r, c = parse_move(txt)
    except Exception:
        r, c = game.fallback_move()
        note = "fallback: parse_error"

    if not game.valid(r, c):
        r, c = game.fallback_move()
        note = "fallback: invalid_move"

    game.play(r, c)

    return {
        "coup": [r, c],
        "grid": game.grid,
        "player": game.player,
        "winner": game.winner(),
        "draw": game.draw(),
        "texte_llm": txt,
        "note": note
    }
