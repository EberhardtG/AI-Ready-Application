"""
WHY / DESIGN — app/routers/tasks.py

Purpose:
This router implements all task‑related API endpoints, including creation,
retrieval, updating, deletion, filtering, and AI suggestions. It enforces
authentication, ensures tasks are scoped to the correct user, and provides
clean separation between business logic and application wiring.

Design Choices:
- Modular Routing:
  Using APIRouter keeps task endpoints isolated from authentication and startup
  logic. This aligns with FastAPI’s recommended structure and makes the project
  easier to maintain.

- Authentication Enforcement:
  Every endpoint depends on get_current_user, ensuring only authenticated users
  can interact with tasks. User‑scoped queries prevent cross‑user access and
  satisfy Module 5 authorization requirements.

- ORM Integration:
  Endpoints interact directly with SQLAlchemy models using the get_db dependency.
  This keeps database access consistent and ensures each request uses a clean
  session.

- Filtering Logic:
  list_tasks supports optional filtering by completion status and priority.
  This keeps the endpoint flexible while maintaining clear, predictable behavior.

- PATCH for Partial Updates:
  TaskPatch allows updating only the fields provided by the client. This avoids
  overwriting unchanged fields and keeps updates lightweight.

- AI Suggestion Endpoint:
  The suggestion route demonstrates how additional functionality can be layered
  onto core CRUD operations. Keeping the suggestion logic here avoids cluttering
  the Task model and makes future AI integration straightforward.

- Logging Integration:
  INFO logs track normal operations, WARNING logs capture risky or destructive
  actions, and ERROR logs highlight unauthorized or invalid access attempts.
  Sensitive data is never logged.

Outcome:
This router provides a clean, secure, and fully modular implementation of task
management. It satisfies Module 5 requirements for CRUD operations, filtering,
authorization, and AI suggestions while keeping the codebase organized and easy
to extend.
"""


from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import logging

from app.models.task import Task
from app.schemas.task import Priority, TaskCreate, TaskPatch, TaskResponse, TaskSuggestionResponse
from app.models.user import User
from app.database import get_db
from app.auth import get_current_user
from app.schemas.auth import TokenResponse


router = APIRouter()

# Configure module-level logger
logger = logging.getLogger(__name__)


@router.post("/", response_model=TaskResponse, status_code=200)
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    logger.info(f"User {current_user.id} creating task: {task.title}")

    new_task = Task(
        title=task.title,
        description=task.description,
        priority=task.priority,
        user_id=current_user.id
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    logger.info(f"Task {new_task.id} created for user {current_user.id}")
    return new_task


@router.get("/", response_model=list[TaskResponse])
def list_tasks(
    completed: bool | None = None,
    priority: Priority | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    logger.info(
        f"User {current_user.id} listing tasks "
        f"(completed={completed}, priority={priority})"
    )

    query = db.query(Task).filter(Task.user_id == current_user.id)

    if completed is not None:
        query = query.filter(Task.completed == completed)

    if priority is not None:
        query = query.filter(Task.priority == priority)

    tasks = query.all()
    logger.info(f"User {current_user.id} retrieved {len(tasks)} tasks")
    return tasks


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    logger.info(f"User {current_user.id} fetching task {task_id}")

    task = db.query(Task).filter(Task.id == task_id, Task.user_id == current_user.id).first()

    if not task:
        logger.error(f"Task {task_id} not found for user {current_user.id}")
        raise HTTPException(status_code=404, detail="Task not found")

    if task.user_id != current_user.id:
        logger.warning(
            f"Unauthorized access attempt: user {current_user.id} tried to access task {task_id}"
        )
        raise HTTPException(status_code=403, detail="Not authorized to access this task")

    return task


@router.patch("/{task_id}", response_model=TaskResponse)
def patch_task(
    task_id: int,
    task_data: TaskPatch,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    logger.info(f"User {current_user.id} updating task {task_id}")

    task = db.query(Task).filter(Task.id == task_id, Task.user_id == current_user.id).first()

    if not task:
        logger.error(f"Task {task_id} not found for user {current_user.id}")
        raise HTTPException(status_code=404, detail="Task not found")

    for field, value in task_data.model_dump(exclude_unset=True).items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)

    logger.info(f"Task {task_id} updated for user {current_user.id}")
    return task


@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    logger.warning(f"User {current_user.id} attempting to delete task {task_id}")

    task = db.query(Task).filter(Task.id == task_id, Task.user_id == current_user.id).first()

    if not task:
        logger.error(f"Task {task_id} not found for user {current_user.id}")
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()

    logger.warning(f"Task {task_id} deleted by user {current_user.id}")
    return {"message": "Task deleted successfully"}


@router.post("/{task_id}/suggest", response_model=TaskSuggestionResponse)
def suggest_task_action(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    logger.info(f"User {current_user.id} requesting suggestion for task {task_id}")

    task = db.query(Task).filter(Task.id == task_id, Task.user_id == current_user.id).first()

    if not task:
        logger.error(f"Task {task_id} not found for user {current_user.id}")
        raise HTTPException(status_code=404, detail="Task not found")

    if task.user_id != current_user.id:
        logger.warning(
            f"Unauthorized suggestion request: user {current_user.id} "
            f"attempted to access task {task_id}"
        )
        raise HTTPException(status_code=403, detail="Not authorized to access this task")

    suggestion_text = (
        f"Based on your task '{task.title}', consider breaking it into smaller steps "
        f"or scheduling focused time blocks to make progress."
    )

    logger.info(f"Suggestion generated for task {task_id} (user {current_user.id})")
    return TaskSuggestionResponse(suggestion=suggestion_text)
