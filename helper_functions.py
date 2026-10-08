"""
WHY / DESIGN — app/utils/helper_function.py

Purpose:
This module provides small, reusable utility functions that support common
operations across the application. These helpers keep logic clean inside routers
and models by centralizing simple transformations and repeated behaviors.

Design Choices:
- now_utc():
  Returns a timezone‑aware UTC timestamp using datetime.now(timezone.utc). This
  avoids naive datetime objects and ensures consistent time handling across the
  API, especially for created_at or updated_at fields.

- clean_text():
  Strips leading and trailing whitespace from user input. Centralizing this avoids
  duplicated `.strip()` calls in routers and ensures consistent preprocessing of
  text fields.

- validate_priority():
  Converts a raw string into a Priority enum. This keeps enum validation logic in
  one place and ensures that incoming values map cleanly to the Task model’s
  Priority field.

- generate_ai_suggestion():
  Provides a placeholder AI suggestion for tasks. Abstracting this into a helper
  function keeps the tasks router clean and makes it easy to replace the placeholder
  with a real AI model later without changing endpoint logic.

Outcome:
These helpers improve readability, reduce duplication, and isolate small pieces of
logic that would otherwise clutter routers or models. They support clean API design
and make future enhancements easier to implement.
"""

from datetime import datetime, timezone
from app.models.task import Priority

def now_utc():
    """Return current UTC timestamp."""
    return datetime.now(timezone.utc)

def clean_text(text: str) -> str:
    """Trim whitespace from user input."""
    return text.strip()

def validate_priority(value: str) -> Priority:
    """Convert a string to a Priority enum."""
    return Priority(value)

def generate_ai_suggestion(title: str) -> str:
    """Placeholder AI suggestion generator."""
    return f"Based on your task '{title}', consider breaking it into smaller steps."
