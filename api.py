# api.py
from fastapi import FastAPI
import requests
import re

from game import GameEngine
from prompt import build_prompt

app = FastAPI()
engine = GameEngine(size=10)


def call_mistral(prompt: str) -> str:
    r = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "mistral", "prompt": prompt, "stream": False},
        timeout=120
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

    raise ValueError(f"No numbers found. Got:\n{txt}")



@app.get("/state")
def state():
    return {"grid": engine.grid, "player": engine.current_player}


@app.post("/reset")
def reset():
    engine.reset()
    return {"ok": True}

from game import EMPTY  

def fallback_move():
    center = engine.size // 2
    best = None
    best_dist = 10**9
    for r in range(engine.size):
        for c in range(engine.size):
            if engine.grid[r][c] == EMPTY:
                d = abs(r - center) + abs(c - center)
                if d < best_dist:
                    best_dist = d
                    best = (r, c)
    return best  # (r,c)

@app.post("/llm-play")
def llm_play():
    prompt = build_prompt(engine.grid, engine.current_player)
    txt = call_mistral(prompt)

    try:
        r, c = parse_move(txt)
    except Exception:
        r, c = fallback_move()
        engine.play(r, c)
        return {
            "coup": [r, c],
            "grid": engine.grid,
            "player": engine.current_player,
            "winner": engine.winner(),
            "draw": engine.draw(),
            "texte_llm": txt,
            "note": "fallback: parse_error"
        }

    if not engine.is_valid_move(r, c):
        r, c = fallback_move()
        engine.play(r, c)
        return {
            "coup": [r, c],
            "grid": engine.grid,
            "player": engine.current_player,
            "winner": engine.winner(),
            "draw": engine.draw(),
            "texte_llm": txt,
            "note": "fallback: invalid_move"
        }

    engine.play(r, c)
    return {
        "coup": [r, c],
        "grid": engine.grid,
        "player": engine.current_player,
        "winner": engine.winner(),
        "draw": engine.draw(),
        "texte_llm": txt,
        "note": "ok"
    }

