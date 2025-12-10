from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import random
from email_utils import send_email
from dbs_data import DBS_KB

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LoginRequest(BaseModel):
    email: str
    password: str

class RegisterRequest(BaseModel):
    email: str
    password: str

class OTPVerify(BaseModel):
    email: str
    otp: str

class ChatRequest(BaseModel):
    message: str

OTP_STORE = {}

def load_users():
    with open("users.json", "r") as f:
        return json.load(f)

def save_users(users):
    with open("users.json", "w") as f:
        json.dump(users, f, indent=2)

@app.post("/register")
def register(data: RegisterRequest):
    users = load_users()
    for u in users:
        if u["email"] == data.email:
            raise HTTPException(status_code=400, detail="Email already registered")

    users.append({"email": data.email, "password": data.password})
    save_users(users)
    return {"message": "Registration successful"}

@app.post("/login")
def login(user: LoginRequest):
    users = load_users()
    for u in users:
        if u["email"] == user.email and u["password"] == user.password:
            otp = str(random.randint(100000, 999999))
            OTP_STORE[user.email] = otp
            send_email(user.email, otp)
            return {"status": "otp_required"}

    raise HTTPException(status_code=400, detail="Invalid email or password")

@app.post("/verify-otp")
def verify_otp(data: OTPVerify):
    if OTP_STORE.get(data.email) == data.otp:
        return {"status": "success"}
    raise HTTPException(status_code=400, detail="Invalid OTP")

@app.post("/chat")
def chat(req: ChatRequest):
    msg = req.message.lower()

    # Match message to knowledge base
    for key in DBS_KB:
        if key in msg:
            return {"reply": DBS_KB[key]}

    # fallback response
    return {"reply": "I am DigiBot, your DBS assistant. I can answer questions about DBS Bank, accounts, loans, digibank, credit cards, and more."}

@app.get("/")
def home():
    return {"message": "Backend running"}
