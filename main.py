from fastapi import FastAPI, Request
from typing import List, Dict
import re
import sqlite3
from datetime import datetime

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


@app.post("/rawToJson")
async def raw_to_json(request: Request) -> List[Dict]:
    """
    Converts raw text input to structured JSON.
    """
    body = await request.body()
    raw_text = body.decode("utf-8").strip()

    # Extract date
    date_match = re.search(r"Controlled Date:\s*(\d{2}-[A-Z]{3}-\d{2})", raw_text)
    if not date_match:
        return {"error": "Controlled Date not found"}
    
    input_date_str = date_match.group(1)  # e.g. 13-JUN-24
    input_date = datetime.strptime(input_date_str, "%d-%b-%y")
    formatted_date = input_date.strftime("%Y/%m/%d 00:00:00")

    # Extract PO lines
    po_lines = re.findall(r"po_number='(\d+)'\s*and\s*po_line_number=(\d+)", raw_text)

    result = []
    for po_number, po_line in po_lines:
        result.append({
            "PO_NUMBER": int(po_number),
            "PO_LINE_NUMBER": int(po_line),
            "INPUT_DATE": formatted_date
        })

    return result