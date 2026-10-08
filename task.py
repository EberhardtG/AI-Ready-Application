"""
WHY / DESIGN — app/schemas/task.py

Purpose:
These Pydantic models define the structure of all task‑related data flowing
through the API. They validate incoming task creation and update payloads,
shape outgoing responses, and ensure consistent typing for priority, timestamps,
and ownership. Centralizing these schemas keeps the API predictable and secure.

Design Choices:
- Priority Enum:
  Defining Priority as a string‑based Enum ensures only valid values ("low",
  "medium", "high") can be used. This prevents invalid priority inputs and keeps
  the API aligned with the Task model’s constraints.

- TaskCreate:
  Enforces required fields and length constraints for title and description.
  Default values for priority and completed provide predictable behavior and
  reduce boilerplate for clients. Example data improves API documentation.

- TaskPatch:
  Allows partial updates by making all fields optional. This keeps PATCH requests
  lightweight and avoids forcing clients to resend unchanged fields.

- TaskResponse:
  Represents the full task object returned to clients, including timestamps and
  user ownership. from_attributes=True enables direct conversion from ORM models,
  and example data clarifies the expected response format.

- TaskSuggestionResponse:
  Provides a simple schema for the AI suggestion endpoint. Keeping this separate
  avoids mixing suggestion output with core task fields and keeps the API clean.

Outcome:
These schemas enforce strong validation, ensure consistent task structure, and
prevent accidental exposure of internal fields. They satisfy Module 5 requirements
for proper CRUD modeling, enum validation, and clear API documentation while
keeping the implementation maintainable and easy to extend.
"""


from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from enum import Enum
from datetime import datetime
from app.models.task import Priority


class Priority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class TaskCreate(BaseModel):
    """Input for creating a task."""
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=2000)
    priority: Priority = Priority.medium
    completed: bool = False

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Finish Module 5 project",
                "description": "Implement Task CRUD and authentication",
                "priority": "high",
                "completed": False
            }
        }
    )


class TaskPatch(BaseModel):
    """Input for partial task update."""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=2000)
    priority: Optional[Priority] = None
    completed: Optional[bool] = None


class TaskResponse(BaseModel):
    """Returned to clients."""
    id: int
    title: str
    description: Optional[str]
    priority: Priority
    completed: bool
    user_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "title": "Finish Module 5 project",
                "description": "Implement Task CRUD and authentication",
                "priority": "high",
                "completed": False,
                "user_id": 3,
                "created_at": "2026-10-06T14:22:00Z",
                "updated_at": "2026-10-06T14:25:00Z"
            }
        }
    )
class TaskSuggestionResponse(BaseModel):
    suggestion: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "suggestion": "Try breaking this task into smaller steps to make it easier to complete."
            }
        }
    )
    
    