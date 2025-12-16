# backend/main.py

import json
import random
import requests
from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from rag_utils import search_kb


# ======================================
# FastAPI App
# ======================================
app = FastAPI(title="DigiBot Backend")


# ======================================
# CORS SETTINGS
# ======================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # dev only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ======================================
# DATA MODELS
# ======================================
class Login(BaseModel):
    email: str
    password: str

class ChatRequest(BaseModel):
    query: str


USERS_FILE = "users.json"


# ======================================
# HELPER FUNCTIONS
# ======================================
def load_users() -> List[dict]:
    try:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []


# ======================================
# FAST LOCAL LLM (OLLAMA – PHI)
# ======================================
def call_llm(prompt: str) -> str:
    """
    Fast local LLM using Ollama (phi model)
    Optimized for speed
    """
    url = "http://localhost:11434/api/generate"

    payload = {
        "model": "phi",
        "prompt": prompt,
        "stream": False,
        "options": {
            "num_predict": 120,   # limit output length (FAST)
            "temperature": 0.2
        }
    }

    response = requests.post(url, json=payload, timeout=120)
    response.raise_for_status()

    return response.json()["response"]


# ======================================
# ROUTES
# ======================================
@app.get("/")
def home():
    return {"message": "Backend Running"}


# -------------------- LOGIN --------------------
@app.post("/login")
def login_user(data: Login):
    users = load_users()

    for u in users:
        if u["email"] == data.email and u["password"] == data.password:
            return {"status": "success"}

    raise HTTPException(status_code=400, detail="Invalid email or password")


# ======================================
# CHATBOT (RAG + FAST LLM FALLBACK)
# ======================================
@app.post("/chat")
def chat(req: ChatRequest):
    try:
        print("\n/chat called →", req.query)

        # 1️⃣ RAG search (k=1 for speed)
        matches = search_kb(req.query, k=1)

        context = matches[0] if matches else ""

        # 2️⃣ VERY SHORT prompt (important for speed)
        prompt = f"""
Answer briefly and clearly.

Context:
{context}

Question:
{req.query}
"""

        # 3️⃣ Call fast local LLM
        answer = call_llm(prompt)

        return {
            "reply": answer,
            "sources": matches if matches else ["LLM fallback (phi)"]
        }

    except Exception as e:
        print("❌ ERROR in /chat:", e)
        raise HTTPException(status_code=500, detail=str(e))


# ======================================
# WARM UP LLM (CRITICAL FOR SPEED)
# ======================================
@app.on_event("startup")
def warmup_llm():
    try:
        print("Warming up local LLM (phi)...")
        call_llm("Say OK")
        print("LLM warm-up completed")
    except Exception as e:
        print("LLM warm-up failed:", e)
