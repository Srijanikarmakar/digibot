from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import random
from email_utils import send_otp

app = FastAPI()

# Allow React frontend to call API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------
# Models
# -------------------

class Register(BaseModel):
    email: str
    password: str

class Login(BaseModel):
    email: str
    password: str

class VerifyOTP(BaseModel):
    email: str
    otp: str

# -------------------
# Helper functions
# -------------------

def load_users():
    try:
        with open("users.json", "r") as f:
            return json.load(f)
    except:
        return []

def save_users(users):
    with open("users.json", "w") as f:
        json.dump(users, f, indent=2)

OTP_STORE = {}    # {email: otp_value}

# -------------------
# Register
# -------------------

@app.post("/register")
def register_user(data: Register):
    users = load_users()

    # Check if email exists
    for u in users:
        if u["email"] == data.email:
            raise HTTPException(status_code=400, detail="Email already registered")

    users.append({
        "email": data.email,
        "password": data.password
    })

    save_users(users)
    return {"message": "Registration successful!"}

# -------------------
# Login (send OTP)
# -------------------

@app.post("/login")
def login_user(data: Login):
    users = load_users()

    for u in users:
        if u["email"] == data.email and u["password"] == data.password:
            otp = str(random.randint(100000, 999999))
            OTP_STORE[data.email] = otp
            send_otp(data.email, otp)  # Email send function
            return {"status": "otp_required"}

    raise HTTPException(status_code=400, detail="Invalid email or password")

# -------------------
# OTP Verification
# -------------------

@app.post("/verify-otp")
def verify_otp(data: VerifyOTP):
    stored = OTP_STORE.get(data.email)

    if stored and stored == data.otp:
        return {"status": "success"}

    raise HTTPException(status_code=400, detail="Invalid OTP")


@app.get("/")
def home():
    return {"message": "Backend Running 🎉"}
