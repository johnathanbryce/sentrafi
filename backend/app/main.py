from fastapi import FastAPI, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.database import get_db

app = FastAPI()


@app.get("/")
def init_app():
    print("Hello world.")
    return {"status": "ok", "service": "sentrafi-backend"}


@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"status": "ok", "db": "connected"}
