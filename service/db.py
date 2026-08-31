import sqlite3
from datetime import datetime

DB_PATH = "service/logs.db"


def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prompt TEXT,
            score REAL,
            verdict TEXT,
            detector TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()


def log_request(prompt: str, score: float, verdict: str, detector: str):
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO requests (prompt, score, verdict, detector, timestamp) VALUES (?, ?, ?, ?, ?)",
        (prompt, score, verdict, detector, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()