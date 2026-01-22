import sqlite3

conn = sqlite3.connect("analytics.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS metrics (
    user_id TEXT,
    campaign TEXT,
    interactions INT
)
""")

conn.commit()
