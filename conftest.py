"""
WHY / DESIGN — test/conftest.py

Purpose:
This module provides the shared pytest fixtures used across the test suite.
It creates an isolated in‑memory SQLite database for every test run and overrides
the application's get_db dependency so tests never touch the real development
database. This ensures deterministic, repeatable, and safe test execution.

Design Choices:
- In‑Memory SQLite:
  Using sqlite:///:memory: with StaticPool keeps all test data isolated and fast.
  StaticPool ensures the same in‑memory database persists across multiple
  connections during a single test, matching FastAPI’s request lifecycle.

- Engine and Session Factory:
  A dedicated test engine and TestingSessionLocal sessionmaker prevent tests from
  interfering with the production engine or SessionLocal defined in app/database.py.

- Dependency Override:
  app.dependency_overrides[get_db] replaces the real database dependency with a
  test‑scoped session. This allows every request made through TestClient to use
  the in‑memory database automatically.

- Per‑Test Lifecycle:
  Base.metadata.create_all() is called before yielding the TestClient, and
  Base.metadata.drop_all() is called afterward. This ensures each test starts with
  a clean schema and no leftover data from previous tests.

Outcome:
This fixture provides a clean, isolated testing environment that mirrors FastAPI’s
real dependency injection behavior. It guarantees reliable test results, prevents
state leakage between tests, and satisfies Module 5 requirements for proper
database isolation in automated testing.
"""


import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app

TEST_DATABASE_URL = "sqlite:///:memory:"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture
def client():
    """Create a TestClient with a temporary in-memory database."""

    # Create the database tables
    Base.metadata.create_all(bind=test_engine)

    # Override the get_db dependency to use the test database
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c

    # Drop the database tables after tests are done
    Base.metadata.drop_all(bind=test_engine)