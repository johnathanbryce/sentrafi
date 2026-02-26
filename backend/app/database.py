# apps connection -- used by FastAPI at runtime

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from app.config import SQL_ECHO


DATABASE_URL = os.environ.get(
    "DATABASE_URL",  # docker compose sets this under "environment"
    "postgresql://sentrafi:sentrafi_dev@localhost:5432/sentrafi_db",  # local fallback
)

# echo=True logs all SQL statements to console — useful for debugging, noisy in prod
engine = create_engine(DATABASE_URL, echo=SQL_ECHO)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# registry - every model inherits this
class Base(DeclarativeBase):
    pass


# fastapi dep — each request gets its own session, guaranteed cleanup on exit
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
