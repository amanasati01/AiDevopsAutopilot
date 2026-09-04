from app.schemas.team_member import TeamMemberCreateRequest
from app.repositories.team_member_repository import TeamMemberRepository
from app.repositories.user_repository import UserRepository
from app.schemas.team_member import TeamMemeberRoleUpdateRequest
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.team_member import TeamMember
from fastapi import HTTPException, status
from uuid import UUID
from app.repositories.team_member_repository import TeamMemberRepository
async def create_member(
    team_id,
    data: TeamMemberCreateRequest,
    db: AsyncSession,
):
    user_repo = UserRepository(db)
    team_member_repo = TeamMemberRepository(db)

    user = await user_repo.get_by_email(data.email)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    is_user_already_member = await team_member_repo.get_membership(
        team_id,
        user.id,
    )

    if is_user_already_member:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User is already a member of this team",
        )

    team_member = TeamMember(
        team_id=team_id,
        user_id=user.id,
        role=data.role,
        status="ACTIVE",
    )

    result = await team_member_repo.create(team_member)

    await db.commit()
    await db.refresh(result)

    return result
async def get_all_team_members(team_id,db:AsyncSession):
    repository = TeamMemberRepository(db)
    members = await repository.get_team_members_by_team_id(team_id)
    if members is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Team members not found",
            )
    return members
async def update_team_member_role(team_id:UUID,member_id:UUID,db:AsyncSession,data:TeamMemeberRoleUpdateRequest):
    repository = TeamMemberRepository(db)
    member = await repository.update_role(member_id,team_id,data)
    if member is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Team member not found",
        )
    await db.commit()
    return member
async def delete_team_member(team_id:UUID,member_id:UUID,db:AsyncSession):
    repository = TeamMemberRepository(db)
    member = await repository.delete_member(member_id,team_id,db)
    return member