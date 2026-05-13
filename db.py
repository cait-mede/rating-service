import sqlite3

DB = "ratings.db"

def conn():
    return sqlite3.connect(DB)

# Create the ratings table if it doesn't already exist
def init():
    c = conn()
    cur = c.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS ratings (
        app_id TEXT NOT NULL,
        entity_id TEXT NOT NULL,
        user_id TEXT NOT NULL,
        rating INTEGER NOT NULL CHECK(rating >= 1 AND rating <= 5),
        comment TEXT,
        PRIMARY KEY (app_id, entity_id, user_id)
    )
    """)

    c.commit()
    c.close()