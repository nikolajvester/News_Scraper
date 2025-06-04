import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect("storage/news_summaries.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS summaries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            url TEXT,
            summary TEXT,
            date TEXT,
            scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def insert_summary(title, url, summary, date=None):
    conn = sqlite3.connect("storage/news_summaries.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO summaries (title, url, summary, date)
        VALUES (?, ?, ?, ?)
    """, (title, url, summary, date))
    conn.commit()
    conn.close()
