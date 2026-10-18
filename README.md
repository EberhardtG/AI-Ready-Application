
# 🚀 FastAPI Task Manager API  
A secure, fully‑tested Task Management API built with **FastAPI**, **JWT authentication**, **SQLAlchemy**, and **Pydantic v2** — now paired with a **Streamlit frontend** (`my_frontend.py`) that provides a clean, interactive UI for managing tasks.

---

## 📌 Features

### 🔐 Authentication & Authorization
- User registration  
- Secure password hashing (Passlib)  
- JWT login + token issuance  
- Protected routes using `HTTPBearer`  
- User‑scoped access (users can only access their own tasks)

### 📝 Task Management (Backend + Frontend)
- Create tasks  
- List tasks with filters (`completed`, `priority`, `search`)  
- Get a single task  
- Update tasks (PATCH)  
- Toggle completion via checkbox  
- Delete tasks  
- AI suggestion endpoint (`/tasks/{id}/suggest`)

### 🎨 Streamlit Frontend (`my_frontend.py`)
- Login screen with session‑based JWT storage  
- Dashboard metrics (total tasks, completed, pending, priority breakdown)  
- Task creation form  
- Interactive task list  
  - Priority filtering  
  - Completed filtering  
  - Search filtering  
  - Completion toggle (checkbox → PATCH)  
  - Delete buttons  
- Automatic UI refresh using `st.rerun()`  
- Clean column‑based layout for task interaction  
- Fully integrated with FastAPI backend

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
- Streamlit UI separated cleanly from API logic

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
├── main.py
└── my_frontend.py   <-- Streamlit UI
```

Tests:

```
app/tests/
│
├── test_tasks.py
└── conftest.py
```

---

## ⚙️ Running the Frontend

### 1. Start the FastAPI backend
```bash
uvicorn app.main:app --reload
```

### 2. Run the Streamlit frontend
```bash
streamlit run app/my_frontend.py
```

### 3. Open the UI  
Navigate to:

```
http://localhost:8501
```

---

## 🧠 Design Decisions

### ✔ Modular Architecture  
Routers, models, schemas, and utilities are separated for clarity and maintainability.

### ✔ Streamlit Frontend Separation  
The UI lives in `my_frontend.py`, keeping presentation logic separate from API logic while still tightly integrated through HTTP requests.

### ✔ Full CRUD Support  
Both backend and frontend support create, read, update, and delete operations — including interactive completion toggling.

### ✔ Dashboard Metrics  
The frontend computes real‑time task analytics for a more professional user experience.

### ✔ JWT Authentication  
Tokens stored in session state allow secure, persistent login across Streamlit reruns.

---

## 💡 Reflection

### **Challenge**
Synchronizing backend CRUD operations with a reactive Streamlit UI.

### **Solution**
Use `st.session_state` for auth persistence and `st.rerun()` after every mutation to keep the UI consistent.

### **What I’d Add With More Time**
- Editable modal for task updates  
- Priority color‑coding  
- Pagination  
- Real AI suggestions using OpenAI or Azure OpenAI  
- Admin roles  
- Refresh tokens  

---

## 📜 Author
Grant Eberhardt

---

