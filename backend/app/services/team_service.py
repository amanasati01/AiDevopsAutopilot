from datetime import datetime,timezone
from app.schemas.team import TeamCreateRequest
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends,HTTPException,status
from app.models.user import User
from app.models.team import Team
from app.models.team_member import TeamMember
from app.repositories.team_member_repository import TeamMemberRepository
from app.repositories.teams_repository import TeamsRepository
async def create_team(
    data: TeamCreateRequest,
    db: AsyncSession,
    current_user: User,
):
    try:
        team_repository = TeamsRepository(db)
        member_repository = TeamMemberRepository(db)

        team = Team(
            name=data.name,
            slug=data.name.lower().strip().replace(" ", "-"),
            owner_id=current_user.id,
        )
        existing_slug =await team_repository.get_by_slug(team.slug)
        if existing_slug:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Slug already exists"
            )
        await team_repository.create(team)

        member = TeamMember(
            team_id=team.id,
            user_id=current_user.id,
            role="OWNER",
            status="ACTIVE",
            joined_at=datetime.now(timezone.utc),
        )

        await member_repository.create(member)

        await db.commit()
        await db.refresh(team)

        return team

    except Exception:
        await db.rollback()
        raise
    
    
    