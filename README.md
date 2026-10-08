
# 🚀 FastAPI Task Manager API  
A secure, fully‑tested Task Management API built with **FastAPI**, **JWT authentication**, **SQLAlchemy**, and **Pydantic v2**.  
Includes complete CRUD operations, user‑scoped authorization, AI‑style task suggestions, and an automated test suite.

---

## 📌 Features

### 🔐 Authentication & Authorization
- User registration  
- Secure password hashing (Passlib)  
- JWT login + token issuance  
- Protected routes using `HTTPBearer`  
- User‑scoped access (users can only access their own tasks)

### 📝 Task Management
- Create tasks  
- List tasks with filters (`completed`, `priority`)  
- Get a single task  
- Update tasks (PATCH)  
- Delete tasks  
- AI suggestion endpoint (`/tasks/{id}/suggest`)

### 🧪 Testing
- Full pytest suite  
- In‑memory SQLite test database  
- Tests for:
  - Registration  
  - Login  
  - Authenticated task creation  
  - User‑scoped filtering  
  - Unauthorized access (403)  
  - Missing token (401)  
  - Nonexistent tasks (404)  
  - Suggestion endpoint  

### 🧱 Clean Architecture
- Routers  
- Models  
- Schemas  
- Auth utilities  
- Config + environment settings  
- Dependency‑injected database sessions  

---

## 📂 Project Structure

```
app/
│
├── routers/
│   ├── auth.py
│   └── tasks.py
│
├── models/
│   ├── user.py
│   └── task.py
│
├── schemas/
│   ├── user.py
│   ├── task.py
│   └── auth.py
│
├── utils/
│   └── helper_function.py
│
├── auth.py
├── database.py
├── config.py
└── main.py
```

Tests:

```
app/tests/
│
├── test_tasks.py
└── conftest.py
```

---

## ⚙️ Installation & Setup

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd fastapi-task-manager
```

### 2. Create a virtual environment
```bash
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
.venv\Scripts\activate      # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the API
```bash
uvicorn app.main:app --reload
```

### 5. Open Swagger UI  
Navigate to:

```
http://localhost:8000/docs
```

---

## 🔥 API Endpoints Overview

### **Auth**
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register` | Register a new user |
| POST | `/auth/token` | Login and receive JWT |
| GET | `/auth/me` | Get current authenticated user |

### **Tasks**
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/tasks` | Create a task |
| GET | `/tasks` | List tasks (with filters) |
| GET | `/tasks/{id}` | Get a specific task |
| PATCH | `/tasks/{id}` | Update a task |
| DELETE | `/tasks/{id}` | Delete a task |
| POST | `/tasks/{id}/suggest` | AI suggestion for a task |

---

## 🧪 Running Tests

```bash
pytest -v
```

You should see output similar to:

```
10 passed, 0 failed
```

The test suite uses an isolated in‑memory SQLite database to ensure clean, repeatable runs.

---

## 🧠 Design Decisions

### ✔ Modular Architecture  
Routers, models, schemas, and utilities are separated for clarity and maintainability.

### ✔ Dependency Injection  
FastAPI’s DI system is used for:
- Database sessions  
- Current user authentication  
- Security dependencies  

This keeps endpoints clean and testable.

### ✔ JWT Authentication  
Tokens store the user ID in the `sub` claim, enabling strict user‑scoped authorization.

### ✔ ORM + Pydantic v2  
Models use SQLAlchemy 2.0 style with `Mapped[]` typing.  
Schemas use `ConfigDict(from_attributes=True)` for clean ORM → Pydantic conversion.

---

## 💡 Reflection

### **Challenge**
Handling user‑scoped authorization correctly.  
Initially, accessing another user’s task returned `404`, but the test suite required `403`.

### **Solution**
Split the logic:
1. Check if the task exists  
2. Check if the user owns it  

This ensures:
- `404` → task doesn’t exist  
- `403` → task exists but belongs to someone else  

### **What I’d Add With More Time**
- Real AI suggestions using OpenAI or Azure OpenAI  
- Task deadlines + reminders  
- Pagination for large task lists  
- Admin roles  
- Refresh tokens  

---

## 📜 Author
Grant Eberhardt
