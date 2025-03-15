from fastapi import FastAPI, HTTPException, Depends, Form
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timedelta
import sqlite3, os

TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 30
DB_PATH = "tokens.db"

def generate_access_token(user_id: str):
    """Функция генерации access-токена (реализуйте свою криптографию)"""
    return f"access_token_{user_id}_{os.urandom(16).hex()}"

def generate_refresh_token(user_id: str):
    """Функция генерации refresh-токена (реализуйте свою криптографию)"""
    return f"refresh_token_{user_id}_{os.urandom(16).hex()}"

def verify_code_challenge(code_verifier: str, code_challenge: str):
    """Функция проверки PKCE (реализуйте свой алгоритм)"""
    return True

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tokens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            token TEXT UNIQUE,
            user_id TEXT,
            expires_at DATETIME
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS refresh_tokens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            token TEXT UNIQUE,
            user_id TEXT,
            expires_at DATETIME
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            client_id TEXT PRIMARY KEY,
            client_secret TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT
        )
    """)
    conn.commit()
    return conn

def store_token(token: str, user_id: str, expires_at: datetime):
    conn = get_db_connection()
    conn.execute("INSERT INTO tokens (token, user_id, expires_at) VALUES (?, ?, ?)", (token, user_id, expires_at))
    conn.commit()
    conn.close()

def revoke_token(token: str):
    conn = get_db_connection()
    conn.execute("DELETE FROM tokens WHERE token = ?", (token,))
    conn.commit()
    conn.close()

app = FastAPI()

@app.post("/authorization")
def authorize(client_id: str, redirect_uri: str, code_challenge: str, username: str = Form(...), password: str = Form(...)):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT password FROM users WHERE username = ?", (username,))
    user = cur.fetchone()
    conn.close()
    if not user or user[0] != password:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    auth_code = os.urandom(16).hex()
    return {"authorization_code": auth_code, "redirect_uri": redirect_uri, "code_challenge": code_challenge}

@app.post("/get_token")
def get_token(client_id: str = Form(...), client_secret: str = Form(...), code: str = Form(...), code_verifier: str = Form(...), code_challenge: str = Form(...)):
    if not verify_code_challenge(code_verifier, code_challenge):
        raise HTTPException(status_code=400, detail="PKCE verification failed")
    access_token = generate_access_token("user_id")
    refresh_token = generate_refresh_token("user_id")
    expires_at = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    store_token(access_token, "user_id", expires_at)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@app.post("/refresh_token")
def refresh(refresh_token: str = Form(...)):
    """Проверяйте и обновляйте токены по вашей криптографии"""
    return {"access_token": generate_access_token("user_id"), "refresh_token": generate_refresh_token("user_id"), "token_type": "bearer"}

@app.post("/revoke_token")
def revoke(access_token: str = Form(...)):
    revoke_token(access_token)
    return {"message": "Token revoked"}

@app.post("/notification")
def notification():
    return {"message": "Notification received"}

@app.get("/api/user_info")
def user_info(token: str):
    """Добавьте проверку токена по вашему алгоритму"""
    return {"user": "user_id"}
