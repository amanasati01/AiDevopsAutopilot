from fastapi import APIRouter,Depends,HTTPException,status
from app.services.project_service import create_project,get_team_projects,get_project_by_projectid,update_project,delete_project
from app.schemas.project import ProjectCreateRequest,ProjectResponse,ProjectUpdateRequest
from app.db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependency import get_current_user
from app.core.authorization import require_team_role
from uuid import UUID
router =  APIRouter(prefix="/teams/{team_id}/projects",
    tags=["Projects"],)

@router.post("",response_model=ProjectResponse,status_code=status.HTTP_201_CREATED)
async def createProject(team_id : UUID,data:ProjectCreateRequest,current_user= Depends(get_current_user),membership = Depends(require_team_role("OWNER","ADMIN")),db:AsyncSession = Depends(get_db)):
    project = await create_project(data,team_id,current_user.id,db)
    return project
@router.get("")
async def getProjects(team_id : UUID,current_user= Depends(get_current_user),membership = Depends(require_team_role("OWNER","ADMIN","MEMBER")),db:AsyncSession = Depends(get_db)):
    projects = await get_team_projects(team_id,db)
    return projects
@router.get("/{project_id}")
async def get_project_by_id(project_id:UUID,team_id:UUID,db:AsyncSession = Depends(get_db)):
    project = await get_project_by_projectid(project_id,team_id,db)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Project not found")
    return project
@router.patch("/{project_id}",response_model=ProjectResponse,status_code=status.HTTP_200_OK)
async def update_project_by_project_id(data:ProjectUpdateRequest,project_id:UUID,current_user= Depends(get_current_user),membership = Depends(require_team_role("OWNER","ADMIN")),db:AsyncSession = Depends(get_db)):
    project = await update_project(data,project_id,db)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Project not found")
    return project
@router.delete("/{project_id}",response_model=ProjectResponse,status_code=status.HTTP_200_OK)
async def delete_project_by_project_id(project_id:UUID,current_user= Depends(get_current_user),membership = Depends(require_team_role("OWNER","ADMIN")),db:AsyncSession = Depends(get_db)):
    project = await delete_project(project_id,db)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Project not found")
    return project