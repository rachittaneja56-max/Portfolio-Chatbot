from fastapi import FastAPI
from pydantic import BaseModel
import json
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware

from app.llm import call_llm, ModelOverloadedError
from app.prompt import build_system_prompt

app = FastAPI()
DATA_PATH = Path("data/portfolio.json")

class Question(BaseModel):
    question: str

def load_portfolio():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://rachits-portfolio24.vercel.app"
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat")
def chat(req: Question):
    portfolio = load_portfolio()

    system_prompt = build_system_prompt(portfolio)

    try:
        answer = call_llm(system_prompt, req.question)

        return {
            "answer": answer.strip()
        }

    except ModelOverloadedError:
        return {
            "answer": "The AI assistant is temporarily unavailable due to high load. Please try again in a moment."
        }
