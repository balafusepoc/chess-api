from fastapi import FastAPI
import sqlite3

app = FastAPI()

# Database connection
def get_db_connection():
    conn = sqlite3.connect("chess_app.db")  # assumes DB exists in same folder
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/")
def read_root():
    return {"message": "Welcome to Chess App API 🚀"}

@app.get("/champions")
def get_champions():
    conn = get_db_connection()
    champions = conn.execute("SELECT * FROM champions").fetchall()
    conn.close()
    return [dict(row) for row in champions]

@app.get("/champions/{champion_id}")
def get_champion(champion_id: int):
    conn = get_db_connection()
    champion = conn.execute(
        "SELECT * FROM champions WHERE id = ?", (champion_id,)
    ).fetchone()
    conn.close()

    if champion is None:
        return {"error": f"No champion found with id {champion_id}"}
    return dict(champion)

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],  # use a restricted origin list in production
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)
