from fastapi import FastAPI, Request
from typing import List, Dict
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import re
import sqlite3
import os
from datetime import datetime


app = FastAPI()

# Database connection
def get_db_connection():
    conn = sqlite3.connect("chess_app.db")  # assumes DB exists in same folder
    conn.row_factory = sqlite3.Row
    return conn

# Get Supabase DB URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("❌ DATABASE_URL not set. Please add it in Render or .env file")

# SQLAlchemy setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Table mapping for 'sid'
class Sid(Base):
    __tablename__ = "sid"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    country = Column(String)
    year = Column(Integer)

# API models
class SidIn(BaseModel):
    name: str
    country: str
    year: int

# Ensure table exists (safety)
Base.metadata.create_all(bind=engine)


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
    Converts raw text input to structured JSON, preserving input order.
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

    result = []
    # Process line by line to keep the order
    for line in raw_text.splitlines():
        po_match = re.search(r"po_number='(\d+)'\s*and\s*po_line_number=(\d+)", line)
        if po_match:
            po_number, po_line = po_match.groups()
            result.append({
                "PO_NUMBER": int(po_number),
                "PO_LINE_NUMBER": int(po_line),
                "INPUT_DATE": formatted_date
            })

    return result

@app.get("/sid")
def get_sid():
    db = SessionLocal()
    records = db.query(Sid).all()
    db.close()
    return [{"id": r.id, "name": r.name, "country": r.country, "year": r.year} for r in records]

@app.post("/sid")
def add_sid(item: SidIn):
    db = SessionLocal()
    record = Sid(name=item.name, country=item.country, year=item.year)
    db.add(record)
    db.commit()
    db.refresh(record)
    db.close()
    return {"id": record.id, "name": record.name}