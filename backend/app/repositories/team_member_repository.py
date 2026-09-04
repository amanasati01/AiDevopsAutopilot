from app.models.team_member import TeamMember
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.team_member import TeamMember
from sqlalchemy import select,update,delete
from app.schemas.team_member import TeamMemeberRoleUpdateRequest
from uuid import UUID
class TeamMemberRepository():
    def __init__(self,db:AsyncSession):
        self.db = db
        
    async def create(self,memeber:TeamMember):
        self.db.add(memeber)
        await self.db.flush()
        return memeber
    async def get_membership(self,teamId,userId)->TeamMember | None:
        result = await self.db.execute(
            select(TeamMember).where(
                TeamMember.team_id == teamId,
                TeamMember.user_id == userId
            )
        )
        return result.scalar_one_or_none()
    async def get_team_members_by_team_id(self,team_id:UUID)->list [TeamMember] | None:
        result = await self.db.execute(
            select(TeamMember).where(
                TeamMember.team_id == team_id
            ).order_by(TeamMember.joined_at.desc())
        )
        return list(result.scalars().all())
    async def update_role(self,member_id:UUID,team_id:UUID,data:TeamMemeberRoleUpdateRequest)->TeamMember | None:
        result = await self.db.execute(
            update(TeamMember).where(TeamMember.team_id == team_id,TeamMember.user_id == member_id).values(role = data.role).returning(TeamMember)
        )
        return result.scalar_one_or_none()
    async def delete_member(self,member_id:UUID,team_id:UUID,db:AsyncSession):
        member = await self.db.execute(
            delete(TeamMember).where(
                TeamMember.team_id == team_id,
                TeamMember.user_id == member_id,
                TeamMember.role != "OWNER"
            ).returning(TeamMember)
        )
        await db.commit()
        return member.scalar_one_or_none()