
# 🚀 Full‑Stack Task Manager  
A secure, full‑stack Task Management application built with **FastAPI**, **JWT authentication**, **SQLAlchemy**, and **Pydantic v2**, paired with a modern **Streamlit frontend** and an optional **OpenAI‑powered AI assistant**.

This project demonstrates complete CRUD functionality, authentication, dashboard analytics, and an interactive chat assistant with streaming responses and mock fallback mode.

---

## 📌 Features

### 🔐 Authentication & Authorization (FastAPI)
- User registration  
- Secure password hashing (Passlib)  
- JWT login + token issuance  
- Protected routes using `HTTPBearer`  
- User‑scoped access (users can only access their own tasks)

---

### 📝 Task Management (Backend + Frontend)
- Create tasks  
- List tasks with filters (`completed`, `priority`, `search`)  
- Get a single task  
- Update tasks (PATCH)  
- Toggle completion via checkbox  
- Delete tasks  
- AI suggestion endpoint (`/tasks/{id}/suggest`)

---

### 🎨 Streamlit Frontend (`app_ai.py`)
- Login screen with session‑based JWT storage  
- Dashboard metrics (total tasks, completed, pending)  
- Dataframe view of tasks  
- Bar chart visualization  
- Task creation form  
- Interactive task list  
  - Priority filtering  
  - Completed filtering  
  - Search filtering  
  - Completion toggle  
  - Delete buttons  
- Automatic UI refresh using `st.rerun()`  
- Clean column‑based layout  
- Offline fallback using `mock_data.py` when backend is unreachable

---

### 🤖 AI Assistant (`ai_chat.py`)
- Real OpenAI streaming responses  
- Mock streaming fallback when API fails or credits are exhausted  
- Customizable system prompt  
- Technical + task‑specific context injection  
- Chat history stored in Streamlit session state  
- Safe error handling and graceful fallback  
- Supports multiple OpenAI models (`gpt‑4o‑mini`, `gpt‑4o`)

---

### 🧪 Testing (Backend)
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

---

## 📂 Project Structure

### Backend (Module 5)
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

### Frontend (Module 6)
```
AI_ready_App/
│
├── app_ai.py           # Main Streamlit app
├── ai_chat.py          # AI assistant + streaming logic
├── api_client.py       # All FastAPI communication
├── mock_data.py        # Offline fallback data
├── requirements.txt    # Frontend dependencies
└── .gitignore          # Ignore secrets, venv, cache
```

---

## ⚙️ Running the Application

### 1. Start the FastAPI backend
```bash
uvicorn app.main:app --reload
```

### 2. Start the Streamlit frontend
```bash
streamlit run app_ai.py
```

### 3. Open the UI  
Visit:

```
http://localhost:8501
```

---

## 🧠 Design Decisions

### ✔ Modular Architecture  
Routers, models, schemas, and utilities are separated for clarity and maintainability.

### ✔ API Client Abstraction  
All HTTP communication is centralized in `api_client.py`, keeping the UI clean.

### ✔ Streamlit Session State  
Used for JWT persistence, chat history, and stable UI behavior across reruns.

### ✔ AI Fallback Mode  
If OpenAI fails (rate limit, invalid key, no credits), the app automatically switches to mock streaming.

### ✔ Dashboard Metrics  
Real‑time analytics give users insight into task completion and workload.

### ✔ Clean Separation  
Backend handles business logic and authentication; frontend handles presentation and interaction.

---

## 💡 Reflection

### **Challenge**
Synchronizing backend CRUD operations with Streamlit’s reactive rerun model.

### **Solution**
Store tokens and chat history in `st.session_state` and use `st.rerun()` after every mutation to keep the UI consistent.

### **What I’d Add With More Time**
- Editable modal for task updates  
- Priority color‑coding  
- Pagination  
- Real AI suggestions using OpenAI or Azure OpenAI  
- Admin roles  
- Refresh tokens  
- WebSocket real‑time updates  

---

## 📜 Author
**Grant Eberhardt**

