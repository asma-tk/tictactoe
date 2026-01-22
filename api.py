from fastapi import FastAPI
from pydantic import BaseModel
import requests
import re
import os

from game import Game
from prompt import build_prompt
from models_config import AZURE_MODELS

app = FastAPI()
game = Game(size=10)


class LlmPlayRequest(BaseModel):
    model: str
    temperature: float = 0.2


def call_azure(prompt: str, deployment: str, temperature: float = 0.2) -> str:
    endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
    api_key = os.environ["AZURE_OPENAI_KEY"]
    api_ver = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")

    url = f"{endpoint}/openai/deployments/{deployment}/chat/completions?api-version={api_ver}"

    r = requests.post(
        url,
        headers={
            "api-key": api_key,
            "Content-Type": "application/json"
        },
        json={
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": temperature
        },
        timeout=120,
    )

    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"]


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


@app.get("/models")
def get_models():
    return AZURE_MODELS


@app.get("/state")
def state():
    return {
        "grid": game.grid,
        "player": game.player,
        "winner": game.winner(),
        "draw": game.draw()
    }


@app.post("/reset")
def reset():
    game.reset()
    return {"ok": True}


@app.post("/llm-play")
def llm_play(req: LlmPlayRequest):
    w = game.winner()
    d = game.draw()
    if w or d:
        return {
            "grid": game.grid,
            "player": game.player,
            "winner": w,
            "draw": d,
            "note": "game_over"
        }

    allowed_ids = {m["id"] for m in AZURE_MODELS}
    if req.model not in allowed_ids:
        return {
            "error": "unknown_model",
            "allowed": list(allowed_ids)
        }

    prompt = build_prompt(game.grid, game.player)
    txt = call_azure(prompt, req.model, req.temperature)

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
