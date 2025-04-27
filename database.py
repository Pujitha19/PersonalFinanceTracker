import sqlite3

def init_db():
    """Initialize SQLite database."""
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            amount REAL,
            category TEXT
        )
    """)
    conn.commit()
    conn.close()

def insert_expense(date, amount, category):
    """Insert an expense into the database."""
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO expenses (date, amount, category) VALUES (?, ?, ?)", (date, amount, category))
    conn.commit()
    conn.close()
    return True