import sqlite3
from pathlib import Path

DB_PATH = Path("users.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # users: id, email, password_hash, is_verified, created_at
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT,
        is_verified INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    # tokens: verification tokens (for email verify), reset OTPs, login OTPs
    c.execute("""
    CREATE TABLE IF NOT EXISTS tokens (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT NOT NULL,
        token TEXT NOT NULL,
        token_type TEXT NOT NULL, -- 'verify', 'otp_login', 'otp_reset'
        expires_at INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    conn.close()
    print("DB initialized at", DB_PATH)

if __name__ == "__main__":
    init_db()
