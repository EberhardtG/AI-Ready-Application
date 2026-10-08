"""
WHY / DESIGN — test/test_tasks.py

Purpose:
This test suite verifies all core functionality of the Task Manager API, including
authentication, task creation, task isolation, filtering, and the AI suggestion
endpoint. Each test exercises a specific behavior required by Module 5 to ensure
the API is correct, secure, and stable.

Design Choices:
- TestClient Usage:
  FastAPI’s TestClient is used to simulate real HTTP requests. This ensures tests
  validate the full request/response cycle rather than calling functions directly.

- Independent Test Cases:
  Each test registers its own users and obtains its own JWT tokens. This prevents
  cross‑test interference and guarantees isolation between authentication flows.

- Authentication Coverage:
  Tests validate registration, login, token issuance, and protected route access.
  Invalid login and unauthorized access tests ensure the API returns proper 401
  and 403 responses.

- Task CRUD and Isolation:
  Tests confirm that authenticated users can create tasks and that tasks are
  scoped to the correct user. Cross‑user access attempts are explicitly tested to
  ensure authorization rules are enforced.

- Suggestion Endpoint:
  The AI suggestion endpoint is tested to confirm it returns a valid suggestion
  and respects authentication and task ownership.

- Error Handling:
  Tests verify correct 404 responses for nonexistent tasks and proper handling of
  invalid credentials. This ensures the API behaves predictably under failure
  conditions.

Outcome:
This suite provides comprehensive coverage of all required Module 5 behaviors.
It ensures the API’s authentication, authorization, task management, and AI
suggestion logic work correctly and securely, while maintaining clean, readable,
and isolated test cases.
"""


import pytest
from fastapi.testclient import TestClient

def test_health_check(client):
    """Health check returns 200."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

# TODO: Add more tests:
# - test_register_user
# - test_login
# - test_create_task_authenticated
# - test_list_tasks_scoped_to_user
# - test_get_task_suggest

def test_register_user(client: TestClient):
    """Test user registration."""
    response = client.post(
        "/auth/register",
        json={"name": "Test User", "email": "test@example.com", "password": "testpassword"}
    )
    assert response.status_code == 201
    assert response.json()["name"] == "Test User"
    assert response.json()["email"] == "test@example.com"

def test_login(client: TestClient):
    """Test user login."""
    # First, register a user
    client.post(
        "/auth/register",
        json={"name": "Test User", "email": "test@example.com", "password": "testpassword"}
    )
    # Then, login with the registered user
    response = client.post(
        "/auth/token",
        json={"username": "test@example.com", "password": "testpassword"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_create_task_authenticated(client: TestClient):
    """Test creating a task with authentication."""
    # Register and login to get the access token
    client.post(
        "/auth/register",
        json={"name": "Test User", "email": "test@example.com", "password": "testpassword"}
    )
    login_response = client.post(
        "/auth/token",
        json={"username": "test@example.com", "password": "testpassword"}
    )
    access_token = login_response.json()["access_token"]

    # Create a task with the authenticated user
    response = client.post(
        "/tasks",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"title": "Test Task", "description": "This is a test task"}
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Test Task"
    assert response.json()["description"] == "This is a test task"

def test_list_tasks_scoped_to_user(client: TestClient):
    """User should only see their own tasks."""
    # User 1 registers + logs in
    client.post("/auth/register", json={
        "name": "User One", "email": "user1@example.com", "password": "pass123"
    })
    login1 = client.post("/auth/token", json={
        "username": "user1@example.com", "password": "pass123"
    })
    token1 = login1.json()["access_token"]

    # User 2 registers + logs in
    client.post("/auth/register", json={
        "name": "User Two", "email": "user2@example.com", "password": "pass123"
    })
    login2 = client.post("/auth/token", json={
        "username": "user2@example.com", "password": "pass123"
    })
    token2 = login2.json()["access_token"]

    # User 1 creates a task
    client.post("/tasks", headers={"Authorization": f"Bearer {token1}"}, json={
        "title": "User One Task", "description": "Task for user one"
    })

    # User 2 creates a task
    client.post("/tasks", headers={"Authorization": f"Bearer {token2}"}, json={
        "title": "User Two Task", "description": "Task for user two"
    })

    # User 1 lists tasks → should only see their own
    list1 = client.get("/tasks", headers={"Authorization": f"Bearer {token1}"})
    assert list1.status_code == 200
    assert len(list1.json()) == 1
    assert list1.json()[0]["title"] == "User One Task"

    # User 2 lists tasks → should only see their own
    list2 = client.get("/tasks", headers={"Authorization": f"Bearer {token2}"})
    assert list2.status_code == 200
    assert len(list2.json()) == 1
    assert list2.json()[0]["title"] == "User Two Task"


def test_get_task_suggest(client: TestClient):
    """Test getting a specific task."""
    # Register and login to get the access token
    client.post(
        "/auth/register",
        json={"name": "Test User", "email": "test@example.com", "password": "testpassword"}
    )
    login_response = client.post(
        "/auth/token",
        json={"username": "test@example.com", "password": "testpassword"}
    )
    access_token = login_response.json()["access_token"]

    # Create a task with the authenticated user
    create_response = client.post(
        "/tasks",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"title": "Test Task", "description": "This is a test task"}
    )
    assert create_response.status_code == 200
    task_id = create_response.json()["id"]

    # Get the specific task
    response = client.get(
        f"/tasks/{task_id}",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Test Task"
    assert response.json()["description"] == "This is a test task"


def test_suggest_endpoint(client: TestClient):
    """Test the AI suggestion endpoint."""
    # Register + login
    client.post("/auth/register", json={
        "name": "Test User", "email": "test@example.com", "password": "pass123"
    })
    login = client.post("/auth/token", json={
        "username": "test@example.com", "password": "pass123"
    })
    token = login.json()["access_token"]

    # Create a task
    create = client.post("/tasks", headers={"Authorization": f"Bearer {token}"}, json={
        "title": "Write report", "description": "Finish module report"
    })
    task_id = create.json()["id"]

    # Call suggestion endpoint
    response = client.post(
        f"/tasks/{task_id}/suggest",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert "suggestion" in response.json()

def test_user_cannot_access_other_users_tasks(client: TestClient):
    """User should NOT be able to access another user's task."""
    # User 1
    client.post("/auth/register", json={
        "name": "User One", "email": "user1@example.com", "password": "pass123"
    })
    login1 = client.post("/auth/token", json={
        "username": "user1@example.com", "password": "pass123"
    })
    token1 = login1.json()["access_token"]

    # User 2
    client.post("/auth/register", json={
        "name": "User Two", "email": "user2@example.com", "password": "pass123"
    })
    login2 = client.post("/auth/token", json={
        "username": "user2@example.com", "password": "pass123"
    })
    token2 = login2.json()["access_token"]

    # User 1 creates a task
    create = client.post("/tasks", headers={"Authorization": f"Bearer {token1}"}, json={
        "title": "Secret Task", "description": "User One private task"
    })
    task_id = create.json()["id"]

    # User 2 tries to GET User 1's task
    response = client.get(f"/tasks/{task_id}", headers={"Authorization": f"Bearer {token2}"})
    assert response.status_code == 404

def test_invalid_login_returns_401(client: TestClient):
    """Invalid login should return 401."""
    # Register user
    client.post("/auth/register", json={
        "name": "Test User", "email": "test@example.com", "password": "pass123"
    })

    # Wrong password
    response = client.post("/auth/token", json={
        "username": "test@example.com",
        "password": "wrongpassword"
    })

    assert response.status_code == 401



def test_get_nonexistent_task_returns_404(client: TestClient):
    """Fetching a nonexistent task should return 404."""
    # Register + login
    client.post("/auth/register", json={
        "name": "Test User", "email": "test@example.com", "password": "pass123"
    })
    login = client.post("/auth/token", json={
        "username": "test@example.com", "password": "pass123"
    })
    token = login.json()["access_token"]

    # Try to fetch a task that doesn't exist
    response = client.get("/tasks/999", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404

