import sqlite3
from datetime import datetime

DB_FILE = "url_shortener.db"


async def init_db():
    print("Creating database...")
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS urls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                original_url TEXT NOT NULL,
                short_url TEXT NOT NULL,
                password TEXT,
                creation_time TEXT NOT NULL,
                expiration_time TEXT NOT NULL
            )
        """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS access_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                short_url TEXT,
                timestamp, TEXT,
                ip_address TEXT
            )
        """
        )
        conn.commit()


def get_db():
    return sqlite3.connect(DB_FILE)
