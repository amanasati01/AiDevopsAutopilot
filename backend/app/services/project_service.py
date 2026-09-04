from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends,HTTPException,status
from app.db.session import get_db
from app.schemas.project import ProjectResponse,ProjectCreateRequest, ProjectUpdateRequest
from app.repositories.project_repository import project_repository
from uuid import UUID
from app.models.project import Project
async def create_project(data:ProjectCreateRequest,team_id:UUID,user_id:UUID,db):
    repository = project_repository(db)
    existing_project = await repository.get_by_slug(team_id,data.slug)
    if existing_project:
        raise ValueError("Project slug already exits")
    project = Project(
        team_id=team_id,
        name=data.name,
        slug=data.slug,
        description=data.description,
        repo_url=data.repo_url,
        default_branch=data.default_branch,
        status="ACTIVE",
        created_by=user_id,
    )
    await repository.create(project)
    await db.commit()
    return project
async def get_team_projects(team_id:UUID,db):
    repository = project_repository(db)
    project = await repository.get_team_projects(team_id)
    return project
async def get_project_by_projectid(project_id:UUID,team_id:UUID,db):
    repository = project_repository(db)
    project = await repository.get_by_id_and_team_id(project_id,team_id)
    return project
async def update_project(data:ProjectUpdateRequest,project_id:UUID,db:AsyncSession):
    repository = project_repository(db)
    updated_project = await repository.update_project(data,project_id)
    return updated_project
async def delete_project(project_id:UUID,db:AsyncSession):
    repository = project_repository(db)
    deleted_project = await repository.delete_project(project_id)
    return deleted_project