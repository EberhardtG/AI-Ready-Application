"""
WHY / DESIGN — api_client.py

Purpose:
This module centralizes all communication between the Streamlit frontend and the
FastAPI backend. It provides a clean, consistent interface for authentication,
task CRUD operations, and user profile retrieval. By isolating API logic here,
the UI remains simple and the application avoids duplicated request code.

Design Choices:
- Single Source of Truth for API Calls:
  All HTTP requests—login, registration, task creation, updates, deletion, and
  profile lookup—are handled in one place. This ensures consistent headers,
  error handling, and timeout behavior across the entire app.

- Streamlit-Friendly Error Reporting:
  Each function catches connection errors, timeouts, and common HTTP status
  codes (400, 401, 403, 404). Errors are surfaced through Streamlit’s UI
  components, giving users immediate feedback without crashing the app.

- JWT-Based Authentication:
  The token stored in Streamlit session state is injected into Authorization
  headers for protected routes. This keeps the frontend stateless while
  maintaining secure access to user-specific resources.

- Graceful Failure Modes:
  Instead of raising exceptions, functions return None or False when operations
  fail. This allows the UI to decide how to respond—showing warnings, switching
  to mock data, or prompting the user to log in again.

Outcome:
The result is a robust, reusable API layer that abstracts away HTTP details,
keeps the Streamlit interface clean, and provides reliable communication with
the FastAPI backend even under network failures or invalid user actions.
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
    
    except requests.exceptions.Timeout:
            st.error("Request timed out. The backend may be slow or overloaded.")
            return None

    if response.status_code == (200, 201):
        return response.json().get("User created")

    if response.status_code ==400:
        try:
            detail= response.json().get("detail", "Registration failed.")
        except ValueError:
            detail= "Registration failed."
            st.error(detail)
            return None

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
    
    except requests.exceptions.Timeout:
            st.error("Request timed out. The backend may be slow or overloaded.")
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
    
    except requests.exceptions.Timeout:
            st.error("Request timed out. The backend may be slow or overloaded.")
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
   
    except requests.exceptions.Timeout:
        st.error("Request timed out. The backend may be slow or overloaded.")
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
   
    except requests.exceptions.Timeout:
        st.error("Request timed out. The backend may be slow or overloaded.")
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
    
    except requests.exceptions.Timeout:
            st.error("Request timed out. The backend may be slow or overloaded.")
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

    except requests.exceptions.Timeout:
            st.error("Request timed out. The backend may be slow or overloaded.")
            return None

    if response.status_code == (200,204):
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
    
    except requests.exceptions.Timeout:
            st.error("Request timed out. The backend may be slow or overloaded.")
            return None

    # Success
    if response.status_code in (200, 201):
        return response.json()

    # Unauthorized (token expired or missing)
    if response.status_code == 401:
        st.warning("Session expired. Please log in again.")
        return None

    # Forbidden — user does NOT own the task
    if response.status_code == 403:
        try:
            detail = response.json().get("detail", "Not authorized to update this task.")
        except ValueError:
            detail = "Not authorized to update this task."
        st.error(detail)
        return None

    # Task not found
    if response.status_code == 404:
        st.error("Task not found.")
        return None

    # Other errors
    st.error(f"Task update failed: {response.text}")
    return None


