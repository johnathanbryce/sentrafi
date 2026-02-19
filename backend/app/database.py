# apps connection -- used by FastAPI at runtime

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


DATABASE_URL = os.environ.get(
    "DATABASE_URL",  # docker compose sets this under "environment"
    "postgresql://sentrafi:sentrafi_dev@localhost:5432/sentrafi_db",  # local fallback
)

engine = create_engine(
    DATABASE_URL, echo=True
)  # echo logs all SQL statements to console TODO - turn off in prod

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
