from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from core.config import settings

DATABASE_URL = settings.DATABASE_URL

# Enable connection pooling and pre-ping to handle disconnected DB sessions gracefully
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db() -> Generator[Session, None, None]:
    """
    Dependency generator for database session management.
    Ensures session closure after request handling.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
