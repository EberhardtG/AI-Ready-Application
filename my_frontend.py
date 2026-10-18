"""
WHY / DESIGN — Streamlit Frontend

Purpose:
Provides a lightweight UI for the FastAPI Task Manager. Handles login,
task creation, browsing, filtering, updating, and deletion using JWT-secured
API calls.

Design Choices:
- Session-Based Auth:
  st.session_state["token"] gates access to protected views and keeps the
  user logged in across reruns.

- Modular API Helpers:
  Each backend action (login, get tasks, update, delete) is isolated for
  clarity, reuse, and consistent error handling.

- Dashboard Metrics:
  Computes totals, completion rate, and priority distribution to give users
  meaningful insight into their tasks.

- Full CRUD UI:
  Forms create tasks, checkboxes toggle completion via PATCH, and delete
  buttons remove tasks. This satisfies the assignment’s CRUD requirement.

- Sidebar Filters:
  Priority, completion status, and search filters allow dynamic task
  refinement without reloading the backend.

- Column Layout:
  Tasks are displayed in three columns (info, completion toggle, delete)
  for clean, scannable interaction.

Outcome:
A simple, reactive, and fully functional frontend demonstrating complete
integration with a JWT-protected FastAPI backend.
"""


import streamlit as st
import requests

API_URL= "http://localhost:8000"

st.set_page_config(page_title="API Task Manager", page_icon="✅", layout="wide")

#--session state INIT--
if "token" not in st.session_state:
    st.session_state["token"] = None
    st.session_state["username"] = None

#--Helper functions--
def register(name: str, email: str, password: str):
    try:
        response = requests.post(
            f"{API_URL}/auth/register",
            json={"name": name, "email": email, "password": password},
            timeout=5
        )
    except requests.exceptions.ConnectionError:
        st.error("Backend unreachable. Please start your FastAPI server.")
        return None

    if response.status_code == (200, 201):
        return response.json().get("User created")

    st.error(f"Registration failed: {response.text}")
    return None
def login(username: str, password:str):
    try:
        response= requests.post(
            f"{API_URL}/auth/token",
            json={"username":username, "password": password}, timeout=5
        )
    except requests.exceptions.ConnectionError:
        st.error("Backend unreachable. Please start your FastAPI server.")
        return None
    if response.status_code in (200,201):
        return response.json().get("access_token")

    st.error("Invalid username or password.")
    return None

def get_me(token: str):
    try:
        response = requests.get(
            f"{API_URL}/auth/me",
            headers={"Authorization": f"Bearer {token}"},
            timeout=5
        )
    except requests.exceptions.ConnectionError:
        st.error("Backend unreachable. Please start your FastAPI server.")
        return None

    if response.status_code in (200, 201):
        return response.json()

    if response.status_code == 401:
        st.warning("Session expired. Please log in again.")
        return None

    st.error(f"Failed to fetch user profile: {response.text}")
    return None

def create_task(token: str, title: str, description: str, priority: str):
    try:
        response = requests.post(
            f"{API_URL}/tasks",
            json={"title": title, "description": description, "priority": priority},
            headers={"Authorization": f"Bearer {token}"},
            timeout=5,
        )
    except requests.exceptions.ConnectionError:
        st.error("Backend unreachable. Please start your FastAPI server.")
        return None

    if response.status_code in (200, 201):

        return response.json()
    if response.status_code == 401:
        st.warning("Session expired. Please log in again.")
        return None
    st.error(f"Task creation failed: {response.text}")
    return None


def get_tasks(token: str):
    try:
        response = requests.get(
            f"{API_URL}/tasks",
            headers={"Authorization": f"Bearer {token}"},
            timeout=5,
        )
    except requests.exceptions.ConnectionError:
        st.error("Backend unreachable. Please start your FastAPI server.")
        return None

    if response.status_code in (200, 201):

        return response.json()

    if response.status_code == 401:
        st.warning("Session expired. Please log in again.")
        return None

    st.error(f"Failed to fetch tasks: {response.text}")
    return None
def get_task_by_id(token: str, task_id: int):
    try:
        response = requests.get(
            f"{API_URL}/tasks/{task_id}",
            headers={"Authorization": f"Bearer {token}"},
            timeout=5
        )
    except requests.exceptions.ConnectionError:
        st.error("Backend unreachable. Please start your FastAPI server.")
        return None

    if response.status_code in (200, 201):
         return response.json()

    if response.status_code == 403:
        st.error("Not authorized to access this task.")
        return None

    if response.status_code == 404:
        st.error("Task not found.")
        return None

    st.error(f"Failed to fetch task: {response.text}")
    return None

def delete_task(token: str, task_id: int):
    try:
        response = requests.delete(
            f"{API_URL}/tasks/{task_id}",
            headers={"Authorization": f"Bearer {token}"},
            timeout=5
        )
    except requests.exceptions.ConnectionError:
        st.error("Backend unreachable. Please start your FastAPI server.")
        return False

    if response.status_code == 204:
        return True

    if response.status_code == 401:
        st.warning("Session expired. Please log in again.")
        return False

    if response.status_code == 403:
        st.error("Not authorized to delete this task.")
        return False

    if response.status_code == 404:
        st.error("Task not found.")
        return False

    st.error(f"Failed to delete task: {response.text}")
    return False

def update_task(token: str, task_id: int, updates: dict):
    try:
        response = requests.patch(
            f"{API_URL}/tasks/{task_id}",
            json=updates,
            headers={"Authorization": f"Bearer {token}"},
            timeout=5
        )
    except requests.exceptions.ConnectionError:
        st.error("Backend unreachable. Please start your FastAPI server.")
        return None

    if response.status_code in (200, 201):
        return response.json()

    st.error(f"Task update failed: {response.text}")
    return None



#--Main ui interface----
def show_metrics(tasks):
    st.subheader("Dashboard")
    st.caption("Task overview")

    total = len(tasks)
    completed = sum(1 for t in tasks if t.get("completed"))
    pending = total - completed

    completion_rate = (completed / total * 100) if total > 0 else 0

    high = sum(1 for t in tasks if t.get("priority") == "high")
    medium = sum(1 for t in tasks if t.get("priority") == "medium")
    low = sum(1 for t in tasks if t.get("priority") == "low")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Tasks", total)
    col2.metric("Completed", completed)
    col3.metric("Pending", pending)

    st.metric("Completion Rate", f"{completion_rate:.1f}%")

    st.write("### Priority Breakdown")
    p1, p2, p3 = st.columns(3)
    p1.metric("High Priority", high)
    p2.metric("Medium Priority", medium)
    p3.metric("Low Priority", low)


def show_create_task_form():
    with st.form("create_task_form"):
        title_input = st.text_input("Title")
        description_input = st.text_area("Description")
        priority_select = st.selectbox("Priority", ["low", "medium", "high"])
        submitted = st.form_submit_button("Create Task")

    if submitted:
        token = st.session_state.get("token")
        if not token:
            st.warning("You must be logged in to create tasks.")
            return

        new_task = create_task(token, title_input, description_input, priority_select)
        if new_task:
            st.success("Task created!")
            st.rerun()


def show_task_list(priority_filter, completed_filter, search_query):
    st.subheader("Your Tasks")
    token = st.session_state.get("token")
    if not token:
        st.warning("You must be logged in to view tasks.")
        return

    tasks = get_tasks(token)
    if tasks is None:
        return

    if len(tasks) == 0:
        st.info("You have no tasks yet.")
        return
#--filter by priority----
    if priority_filter != "all":
        tasks = [t for t in tasks if t.get("priority") == priority_filter]
    # -----------------------------
    # COMPLETED FILTERING
    # -----------------------------
    if completed_filter == "completed":
        tasks = [t for t in tasks if t.get("completed") is True]

    elif completed_filter == "not completed":
        tasks = [t for t in tasks if t.get("completed") is False]

        # -----------------------------
    # SEARCH FILTERING
    # -----------------------------
    if search_query:
        q = search_query.lower()
        tasks = [
            t for t in tasks
            if q in t.get("title", "").lower()
            or q in t.get("description", "").lower()
        ]



    for task in tasks:
        col1, col2, col3 = st.columns([4, 1, 1])

        with col1:
            st.write(f"**{task['title']}**")
            st.write(task.get("description", ""))
            st.write(f"Priority: `{task.get('priority', 'low')}`")

        with col2:
    # Interactive completed toggle
         new_status = st.checkbox(
        "Done",
        value=task.get("completed", False),
        key=f"complete_{task['id']}"
    )

    # If user toggles the checkbox, update the task
    if new_status != task.get("completed"):
        token = st.session_state["token"]
        update_task(token, task["id"], {"completed": new_status})
        st.rerun()


        with col3:
            if st.button("🗑️ Delete", key=f"delete_{task['id']}"):
                token = st.session_state["token"]
                if delete_task(token, task["id"]):
                    st.success("Task deleted!")
                    st.rerun()

#---Auth Gate---
st.title("Task Manager")

# AUTH GATE
if st.session_state["token"] is None:
    st.subheader("Login")
    username = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        token = login(username, password)
        if token:
            st.session_state["token"] = token
            st.rerun()
else:
    user = get_me(st.session_state["token"])
    if user:
        st.sidebar.success(f"Logged in as {user['email']}")


#---Sidebar Controls---
    priority_filter = st.sidebar.selectbox("Filter by priority", ["all", "low", "medium", "high"])
    completed_filter = st.sidebar.selectbox("Completed?", ["all", "completed", "not completed"])
    search_query = st.sidebar.text_input("Search tasks")
    st.sidebar.button("Logout", on_click=lambda: st.session_state.clear())

tasks = get_tasks(st.session_state["token"])

show_create_task_form()
show_metrics(tasks)
show_task_list(priority_filter, completed_filter, search_query)


