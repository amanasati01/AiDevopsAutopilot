from app.models.project import Project
from app.schemas.project import ProjectCreateRequest,ProjectUpdateRequest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from fastapi import HTTPException,status
from uuid import UUID
class project_repository:
    def __init__(self,db:AsyncSession):
        self.db = db
    async def create(self,project:Project)->Project:
        self.db.add(project)
        await self.db.flush()
        await self.db.refresh(project)
        return project
    async def get_by_id(self,project_id:UUID)->Project|None:
        result = await self.db.execute(
            select(Project).where(
                Project.id == project_id
            )
        )
        return result.scalar_one_or_none()
    async def get_by_slug(
        self,
        team_id: UUID,
        slug: str,
    ) -> Project | None:

        result = await self.db.execute(
            select(Project).where(
                Project.team_id == team_id,
                Project.slug == slug,
            )
        )

        return result.scalar_one_or_none()
    async def get_team_projects(
        self,
        team_id: UUID,
    ) -> list[Project]:

        result = await self.db.execute(
            select(Project)
            .where(Project.team_id == team_id)
            .order_by(Project.created_at.desc())
        )

        return list(result.scalars().all())
    async def get_by_id_and_team_id(
        self,
        project_id:UUID,
        team_id : UUID
    ):
        result = await self.db.execute(
            select(Project)
            .where(
                Project.id == project_id,
                Project.team_id == team_id)
        )
        return result.scalar_one_or_none()
    async def update_project(self,data:ProjectUpdateRequest,project_id:UUID):
        result =await self.db.execute(
            update(Project).where(Project.id == project_id).values(data.model_dump(exclude_unset=True)).returning(Project)
        )
        updated_project = result.scalar_one_or_none()
        if updated_project:
            await self.db.commit()
        
        return updated_project
    async def delete_project(self,project_id:UUID):
            result =await self.db.execute(
                delete(Project).where(Project.id == project_id).returning(Project)
            )
            deleted_project = result.scalar_one_or_none()
            if deleted_project:
                await self.db.commit()
            
            return deleted_project
        
        