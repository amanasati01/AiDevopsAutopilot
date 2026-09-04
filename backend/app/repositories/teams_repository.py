from sqlalchemy.ext.asyncio import AsyncSession
from app.models.team import Team
from sqlalchemy import select
class TeamsRepository():
    def __init__(self,db:AsyncSession):
        self.db = db
    async def create(self,team:Team):
        self.db.add(team)
        await self.db.flush()
        return team
    async def get_by_slug(self,slug):
        result =await self.db.execute(
            select(Team).where(Team.slug == slug)
        )
        return result.scalar_one_or_none()
    