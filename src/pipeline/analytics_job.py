import sqlite3

def update_metrics(user_id, campaign):
    conn = sqlite3.connect("analytics.db")
    cur = conn.cursor()

    cur.execute("""
    SELECT interactions FROM metrics
    WHERE user_id=? AND campaign=?
    """, (user_id, campaign))

    row = cur.fetchone()

    if row:
        cur.execute("""
        UPDATE metrics SET interactions = interactions + 1
        WHERE user_id=? AND campaign=?
        """, (user_id, campaign))
    else:
        cur.execute("""
        INSERT INTO metrics VALUES (?, ?, 1)
        """, (user_id, campaign))

    conn.commit()
    conn.close()
