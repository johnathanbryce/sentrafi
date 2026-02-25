from fastapi import FastAPI, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.database import get_db
from fastapi.middleware.cors import CORSMiddleware

# apis
from app.api.endpoints import auth

app = FastAPI(
    title="SentraFi",
    description="AI-powered finance document analyzation and tracking",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[""],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# instantiate routes:
app.include_router(auth.router, prefix="/api/v1", tags=["auth"])


@app.get("/")
def init_app():
    print("Hello world.")
    return {"status": "ok", "service": "sentrafi-backend"}


@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"status": "ok", "db": "connected"}
