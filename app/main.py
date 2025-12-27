from fastapi import FastAPI
from pydantic import BaseModel
import json
from pathlib import Path
from app.llm import call_gemini, ModelOverloadedError
from app.prompt import build_system_prompt 
from app.classifier import classify_domains
from app.context import extract_context
from fastapi.middleware.cors import CORSMiddleware


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
        "rachits-portfolio24.vercel.app/"  
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/chat")
def chat(req: Question):
    portfolio = load_portfolio()

    domains = classify_domains(req.question)

    if not domains:
        return {
            "answer": "I can only answer questions based on the information available in my portfolio."
        }

    context = extract_context(portfolio, domains)

    system_prompt = build_system_prompt(context)

    try:
       answer = call_gemini(system_prompt, req.question)

       return {
        "domains": domains,
        "answer": answer.strip()
        }

    except ModelOverloadedError:
       return {
        "answer": "The AI assistant is temporarily unavailable due to high load. Please try again in a moment."
      }