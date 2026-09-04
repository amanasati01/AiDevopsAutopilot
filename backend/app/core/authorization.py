from uuid import UUID
from app.db.session import get_db
from fastapi import Depends
from app.core.dependency import get_current_user
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.repositories.team_member_repository import TeamMemberRepository
from fastapi import HTTPException,status
def require_team_role(*allowed_roles: str):

    async def checker(
        team_id: UUID,
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db),
    ):
        repository = TeamMemberRepository(db)

        membership = await repository.get_membership(
            team_id,
            current_user.id,
        )

        if membership is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not a member of this team",
            )

        if membership.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission for this action",
            )

        return membership

    return checker