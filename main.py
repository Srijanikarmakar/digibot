# backend/main.py

import json
import requests
from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from rag_utils import search_kb

# ======================================
# FASTAPI APP
# ======================================
app = FastAPI(title="DigiBot Backend")

# ======================================
# CORS SETTINGS
# ======================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # dev only
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


# ======================================
# USER DATA
# ======================================
USERS_FILE = "users.json"


def load_users() -> List[dict]:
    try:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []


# ======================================
# FAST LOCAL LLM (OLLAMA - PHI)
# ======================================
def call_llm(prompt: str) -> str:
    """
    Calls local Ollama LLM (phi model)
    """
    url = "http://localhost:11434/api/generate"

    payload = {
        "model": "phi",
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(url, json=payload, timeout=60)
    response.raise_for_status()

    return response.json().get("response", "")


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


# -------------------- CHATBOT --------------------
@app.post("/chat")
def chat(req: ChatRequest):
    try:
        print("\n/chat called:", req.query)

        # 1️Vector search (FAISS)
        matches = search_kb(req.query, k=1)
        context = matches[0] if matches else ""

        # 2️ Optimized prompt (fast)
        prompt = f"""
Answer briefly and clearly.

Context:
{context}

Question:
{req.query}
"""

        # 3️ Call local LLM
        answer = call_llm(prompt)

        return {
            "reply": answer,
            "sources": matches if matches else ["LLM fallback (phi)"]
        }

    except Exception as e:
        print("ERROR:", e)
        raise HTTPException(status_code=500, detail=str(e))
