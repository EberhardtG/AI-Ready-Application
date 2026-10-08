"""
WHY / DESIGN — database.py

Purpose:
This module centralizes all SQLAlchemy database configuration for the project.
It defines the engine, session factory, declarative base, and the get_db
dependency used throughout the API. Keeping database setup isolated here ensures
consistent connection handling and prevents duplication across routers and models.

Design Choices:
- Environment‑Driven DATABASE_URL:
  The database URL is loaded from environment variables so the API can switch
  between development, testing, and production databases without code changes.

- Single Engine Initialization:
  The SQLAlchemy engine is created once at import time and reused across the
  application. This avoids unnecessary reconnections and ensures efficient
  resource usage.

- SessionLocal Factory:
  sessionmaker is configured with autocommit=False and autoflush=False to give
  the API explicit control over transactions. Each request receives its own
  session, preventing cross‑request interference.

- Declarative Base:
  Base is defined here so all ORM models share the same metadata. This allows
  main.py to create tables cleanly and keeps model definitions consistent.

- get_db Dependency:
  get_db yields a database session for the duration of each request and guarantees
  the session is closed afterward. This pattern integrates cleanly with FastAPI’s
  dependency injection system and prevents connection leaks.

Outcome:
This module provides a clean, reliable foundation for all database operations.
It satisfies Module 5 requirements for proper SQLAlchemy setup, environment‑based
configuration, and safe per‑request session management.
"""


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase
from typing import Generator
import os

# TODO: Load DATABASE_URL from environment (use python-dotenv or os.getenv)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./taskmanager.db")

# TODO: Create the engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# TODO: Create SessionLocal
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass


# TODO: Implement get_db
def get_db() -> Generator[Session, None, None]:
    """Provides a DB session per request lifecycle."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
