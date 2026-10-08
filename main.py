"""
WHY / DESIGN — main.py

Purpose:
main.py serves as the application entry point. It initializes the FastAPI app,
loads environment‑based configuration, sets up database tables, configures CORS,
and registers all routers. Keeping this wiring in one place ensures predictable
startup behavior and a clean separation between infrastructure and business logic.

Design Choices:
- Centralized App Initialization:
  The FastAPI() instance is created here so global settings (title, description,
  version, middleware, routers) are defined in a single, authoritative location.

- Environment‑Driven Configuration:
  SECRET_KEY, ALGORITHM, and DATABASE_URL are loaded from settings, allowing
  secure, environment‑specific configuration without hard‑coding secrets.

- CORS Middleware:
  CORS is explicitly scoped to the frontend origin (localhost:3000). This avoids
  insecure wildcard origins while enabling browser clients to interact with the API.

- Database Table Creation:
  Base.metadata.create_all(bind=engine) initializes tables at startup. This is
  acceptable for a learning project and avoids migration complexity while ensuring
  models are ready before requests hit the API.

- Modular Routing:
  Routers for auth and tasks are imported and registered with prefixes. This keeps
  authentication, task logic, and application wiring decoupled, following FastAPI’s
  recommended modular structure.

- Health Check Endpoint:
  The root ("/") endpoint provides a lightweight status check used by tests and
  deployment environments to verify the API is running.

Outcome:
This structure keeps main.py small, readable, and focused on application wiring.
It satisfies Module 5 requirements for configuration, routing, and project
organization while remaining easy to maintain and extend.
"""




from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from app.database import engine, Base
from app.config import settings



DATABASE_URL = settings.DATABASE_URL


from app.routers import auth, tasks

print("Loaded secret:", settings.SECRET_KEY)
print("Loaded algorithm:", settings.ALGORITHM)
print("Loaded access token expiry minutes:", settings.ACCESS_TOKEN_EXPIRE_MINUTES)

app = FastAPI(
    title="AI-Ready Task Manager",
    description="A task management API with JWT auth and an AI suggestion endpoint.",
    version="1.0.0",
)

# TODO: Configure CORS (specific origins, not *)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # TODO: update for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(tasks.router, prefix="/tasks", tags=["tasks"])


@app.get("/", tags=["health"])
def health_check():
    """Health check endpoint."""
    return {"status": "ok", "message": "Task Manager API is running"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
