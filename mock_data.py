# mock_data.py
"""
Offline fallback data for development when the FastAPI backend
is not running. This allows the dashboard, dataframe, and chart
to render without API calls.

Used only when API requests fail or when running in mock mode.
"""

# Example mock user
MOCK_USER = {
    "id": 1,
    "name": "Offline User",
    "email": "offline@example.com"
}

# Example mock tasks
MOCK_TASKS = [
    {
        "id": 1,
        "title": "Mock Task 1",
        "description": "This is a sample task for offline mode.",
        "priority": "high",
        "completed": False
    },
    {
        "id": 2,
        "title": "Mock Task 2",
        "description": "Another offline task example.",
        "priority": "medium",
        "completed": True
    },
    {
        "id": 3,
        "title": "Mock Task 3",
        "description": "Useful for testing charts and metrics.",
        "priority": "low",
        "completed": False
    }
]
