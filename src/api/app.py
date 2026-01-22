from fastapi import FastAPI
import sqlite3

app = FastAPI()

@app.get("/recommendations/{user_id}")
def recommend(user_id: str):
    conn = sqlite3.connect("analytics.db")
    cur = conn.cursor()

    cur.execute("""
    SELECT campaign, interactions
    FROM metrics
    WHERE user_id=?
    ORDER BY interactions DESC
    LIMIT 5
    """, (user_id,))

    data = cur.fetchall()
    conn.close()

    return {
        "user_id": user_id,
        "recommendations": data
    }

# health check endpoint later
