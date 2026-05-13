from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from db import init, conn

app = FastAPI()
init()


class Rating(BaseModel):
    app_id: str
    entity_id: str
    user_id: str
    rating: int
    comment: str | None = None

# POST /ratings
@app.post("/ratings")
def upsert_rating(r: Rating):
    # Check if rating is between 1 and 5
    if r.rating < 1 or r.rating > 5:
        raise HTTPException(
            status_code=400,
            detail="Rating must be between 1 and 5"
        )

    # Connect to DB
    c = conn()
    cur = c.cursor()

    cur.execute("""
    INSERT INTO ratings (app_id, entity_id, user_id, rating, comment)
    VALUES (?, ?, ?, ?, ?)
    ON CONFLICT(app_id, entity_id, user_id)
    DO UPDATE SET
        rating=excluded.rating,
        comment=excluded.comment
    """, (r.app_id, r.entity_id, r.user_id, r.rating, r.comment))

    # Disconnect from DB and return status
    c.commit()
    c.close()

    return {"status": "upserted"}

# GET /ratings
@app.get("/ratings")
def get_ratings(app_id: str, entity_id: str):
    # Connect to DB
    c = conn()
    cur = c.cursor()

    cur.execute("""
    SELECT user_id, rating, comment
    FROM ratings
    WHERE app_id=? AND entity_id=?
    """, (app_id, entity_id))

    rows = cur.fetchall()
    c.close()

    return {
        "app_id": app_id,
        "entity_id": entity_id,
        "ratings": rows
    }

# DELETE /ratings
@app.delete("/ratings")
def delete_rating(app_id: str, entity_id: str, user_id: str):
    # Connect to DB
    c = conn()
    cur = c.cursor()

    cur.execute("""
    DELETE FROM ratings
    WHERE app_id=? AND entity_id=? AND user_id=?
    """, (app_id, entity_id, user_id))

    # If no result found, return 404
    if cur.rowcount == 0:
        c.close()
        raise HTTPException(status_code=404, detail="Not found")

    c.commit()
    c.close()

    return {"status": "deleted"}