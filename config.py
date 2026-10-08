"""
WHY / DESIGN — config.py

Purpose:
This module centralizes all environment‑driven configuration for the application.
It loads secrets, database URLs, and security settings using Pydantic Settings,
ensuring the API is configurable without modifying source code. This keeps
sensitive values out of the repository and satisfies Module 5 requirements for
environment‑based configuration.

Design Choices:
- Pydantic BaseSettings:
  Using BaseSettings automatically loads values from environment variables and
  supports type validation. This prevents misconfiguration and keeps settings
  strongly typed.

- .env File Support:
  model_config specifies env_file=".env", allowing local development to use a
  simple .env file while production can rely on real environment variables.

- Explicit Fields:
  DATABASE_URL, SECRET_KEY, ALGORITHM, and ACCESS_TOKEN_EXPIRE_MINUTES are
  defined as typed fields. This makes configuration predictable and ensures
  JWT creation, database setup, and authentication logic all pull from a single
  source of truth.

- Extra="ignore":
  Ignoring unknown environment variables prevents accidental failures when
  deployment environments include additional settings unrelated to this project.

Outcome:
This module provides a clean, reliable configuration layer that keeps secrets
and environment‑specific values out of the codebase. It supports secure JWT
authentication, flexible database configuration, and consistent application
behavior across development, testing, and production.
"""



from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str = Field(default="sqlite:///./taskmanager.db")
    SECRET_KEY: str = Field(default="change-this-to-a-long-random-string-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
