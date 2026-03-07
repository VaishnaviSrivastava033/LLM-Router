# FastAPI server, entry point

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv


app = FastAPI(title="LLM Router")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Models ──────────────────────────────────────────────
SIMPLE_MODEL  = "llama-3.1-8b-instant"
COMPLEX_MODEL = "llama-3.3-70b-versatile"

# ── Schemas ─────────────────────────────────────────────
class ChatRequest(BaseModel):
    message: str
    api_key: str          # user pastes key in the UI

class ChatResponse(BaseModel):
    message: str
    routed_to: str
    complexity: str
    model_label: str

# ── Helpers ─────────────────────────────────────────────
CLASSIFIER_PROMPT = """You are a prompt complexity classifier.
Classify the following user prompt as ONLY 'simple' or 'complex'.

Simple  = greetings, small talk, basic facts, short one-line questions
Complex = analysis, coding, reasoning, architecture, multi-step problems

Respond with EXACTLY one word: simple  OR  complex

Prompt: {prompt}"""

def get_client(api_key: str) -> Groq:
    return Groq(api_key=api_key)

def classify(client: Groq, message: str) -> str:
    res = client.chat.completions.create(
        model=SIMPLE_MODEL,
        messages=[{"role": "user", "content": CLASSIFIER_PROMPT.format(prompt=message)}],
        max_tokens=10,
    )
    text = res.choices[0].message.content.strip().lower()
    return "complex" if "complex" in text else "simple"

def call_model(client: Groq, model: str, message: str) -> str:
    res = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": message}],
    )
    return res.choices[0].message.content

# ── Routes ───────────────────────────────────────────────
@app.get("/")
def health():
    return {"status": "LLM Router running"}

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    client     = get_client(req.api_key)
    complexity = classify(client, req.message)

    if complexity == "simple":
        model       = SIMPLE_MODEL
        model_label = "Llama 3 8B  ⚡ fast"
    else:
        model       = COMPLEX_MODEL
        model_label = "DeepSeek-R1 70B  🧠 reasoning"

    reply = call_model(client, model, req.message)
    return ChatResponse(message=reply, routed_to=model, complexity=complexity, model_label=model_label)




