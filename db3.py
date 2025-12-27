import sqlite3

conn = sqlite3.connect("city.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY
)
""")
conn.commit()

def user_exists(user_id: int) -> bool:
    cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
    return cursor.fetchone() is not None

def add_user(user_id: int):
    cursor.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
    conn.commit()
