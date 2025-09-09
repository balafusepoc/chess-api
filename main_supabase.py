from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# FastAPI app
app = FastAPI()

# Get DB URL from environment variable
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
def root():
    return {"message": "Supabase + FastAPI is working!"}

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