import sqlite3
from datetime import datetime
import json

def url_exists(url):
    conn = sqlite3.connect("storage/news_summaries.db")
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM summaries WHERE url = ?", (url,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists

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
            primary_category TEXT,
            secondary_categories TEXT,
            source TEXT,
            scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def insert_summary(title, url, summary, date=None, primary_category=None, secondary_categories=None, source=None):
    conn = sqlite3.connect("storage/news_summaries.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO summaries (title, url, summary, date, primary_category, secondary_categories, source)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
    title,
    url,
    summary,
    date,
    primary_category,
    json.dumps(secondary_categories) if secondary_categories else None,
    source
    ))
    conn.commit()
    conn.close()
