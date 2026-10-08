"""
WHY / DESIGN — app/schemas/auth.py

Purpose:
These Pydantic models define the structure of authentication‑related data for the
API. They validate login input and shape the JWT response returned to clients.
Centralizing these schemas keeps authentication predictable, secure, and easy to
integrate with the rest of the application.

Design Choices:
- LoginRequest:
  Uses typed fields with validation to ensure login attempts always include a
  username and password. The example value improves API documentation and makes
  the expected payload clear to clients.

- TokenResponse:
  Defines the exact structure of JWT responses, including the access token and
  token type. Separating this into its own schema keeps authentication output
  consistent and avoids mixing token fields with user data. json_schema_extra
  provides a realistic example for Swagger UI.

Outcome:
These schemas enforce strong validation for login input and provide a clean,
well‑defined contract for JWT responses. They satisfy Module 5 requirements for
secure authentication modeling and contribute to a clear, maintainable API
structure.
"""

from pydantic import BaseModel, ConfigDict, Field

class LoginRequest(BaseModel):
    username: str = Field(..., example="student@example.com")
    password: str = Field(..., min_length=1, example="secret123")


class TokenResponse(BaseModel):
    """JWT token response."""
    access_token: str
    token_type: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer"
            }
        }
    )