from fastapi import FastAPI
from app.api.routes.health import router as health_router
from app.api.routes.auth import router as auth_router
from app.api.routes.teams import router as teams_router
from app.api.routes.projects import router as projects_router
from app.api.routes.github import router as github_router
app = FastAPI(title="AI Devops Autopilot")
app.include_router(health_router)
app.include_router(auth_router)
app.include_router(teams_router)
app.include_router(projects_router)
app.include_router(github_router)