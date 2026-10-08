"""
WHY / DESIGN — app/schemas/user.py

Purpose:
These Pydantic models define the structure of user‑related data flowing through
the API. They validate incoming registration and login payloads, shape outgoing
responses, and ensure sensitive fields (like passwords) are never returned to
clients. Centralizing these schemas keeps the API consistent and secure.

Design Choices:
- UserCreate:
  Validates registration input with typed fields and constraints. Using EmailStr
  ensures proper email formatting, and password/name length requirements enforce
  basic data quality before reaching the database layer.

- UserResponse:
  Represents the safe, public-facing user object. Passwords are intentionally
  omitted, and from_attributes=True allows ORM models to be converted directly
  into response objects. json_schema_extra provides a clear example for API docs.



Outcome:
These schemas enforce strong validation, prevent accidental exposure of sensitive
data, and provide a clean contract between the API and its clients. They satisfy
Module 5 requirements for secure user modeling and contribute to a well‑structured,
maintainable FastAPI application.
"""


from pydantic import BaseModel, ConfigDict, EmailStr, Field

class UserCreate(BaseModel):
    """Registration input."""
    name: str = Field(..., min_length=1, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)


class UserResponse(BaseModel):
    """Returned to clients — no password fields."""
    id: int
    name: str
    email: EmailStr
    # model_config = ConfigDict(from_attributes=True) this is the same as the below, but the below is more explicit and allows for example data
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "name": "Grant",
                "email": "grant@example.com"
            }
        }
    )



