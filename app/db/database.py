import sqlite3
from pathlib import Path

DB_PATH = Path("data/expynse.db")


def get_connection():
    DB_PATH.parent.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY,
        date TEXT,
        amount REAL,
        currency TEXT,
        bank_category TEXT,
        transaction_type TEXT,
        counter_account TEXT,
        counter_name TEXT,
        transaction_code TEXT,
        description TEXT,
        user_category TEXT,
        UNIQUE(date, amount, transaction_code)
    )
    """)

    cur.execute("""
    CREATE VIRTUAL TABLE IF NOT EXISTS transactions_fts
    USING fts5(description, counter_name, content='transactions', content_rowid='id')
    """)

    conn.commit()
    conn.close()