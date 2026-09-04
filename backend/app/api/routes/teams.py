from fastapi import APIRouter,Depends,status,HTTPException
from app.schemas.team import TeamResponse,TeamCreateRequest
from app.db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.team_service import create_team
from app.services.team_member_service import create_member,update_team_member_role,delete_team_member,get_all_team_members
from app.core.dependency import get_current_user
from app.models.user import User
from app.core.authorization import require_team_role
from uuid import UUID
from app.schemas.team_member import TeamMemberResponse,TeamMemberCreateRequest
from datetime import datetime,timezone,UTC
from app.schemas.team_member import TeamMemeberRoleUpdateRequest
router = APIRouter(
    prefix="/teams",
    tags=["Teams"]
)
@router.post("",response_model=TeamResponse,status_code=status.HTTP_201_CREATED)
async def createTeam(data:TeamCreateRequest,db:AsyncSession=Depends(get_db),current_user:User=Depends(get_current_user)):
    team = await create_team(data,db,current_user)
    if team is None:
        raise HTTPException(
            status_code=409,detail="Something went wrong"
        )
    return TeamResponse(
        id = str(team.id),
        name=team.name,
        slug = team.slug,
        owner_id=str(team.owner_id)
    )
@router.get("/{team_id}/owner-check")
async def owner_check(
    team_id: UUID,
    membership = Depends(require_team_role("OWNER")),
):
    return {
        "message": "You are the owner of this team",
        "role": membership.role,
    }
@router.post("/{team_id}/members",response_model=TeamMemberResponse,status_code=status.HTTP_201_CREATED)
async def CreateTeamMember(team_id,data:TeamMemberCreateRequest,db:AsyncSession=Depends(get_db),current_user=Depends(get_current_user),memberShip= Depends(require_team_role("OWNER","AMDIN"))):
    result = await create_member(team_id,data,db)
    member =  TeamMemberResponse(
    id=result.id,
    team_id=result.team_id,
    user_id=result.user_id,
    role=result.role,
    joined_at=datetime.now(timezone.utc),
    invited_by=current_user.id,
    )
    return member
@router.get("/{team_id}/members",status_code=status.HTTP_200_OK)
async def getMembers(team_id,db:AsyncSession=Depends(get_db),current_user=Depends(get_current_user),memberShip= Depends(require_team_role("OWNER","ADMIN","MEMBER"))):
    members = await get_all_team_members(team_id,db)
    return members
@router.patch("/{team_id}/members/{member_id}")
async def updateRole(team_id:UUID,
                     member_id:UUID,
                     data:TeamMemeberRoleUpdateRequest,
                     db:AsyncSession=Depends(get_db),
                     current_user:User = Depends(get_current_user),
                     membership= Depends(require_team_role("OWNER","ADMIN"))
                     ):
    member = await update_team_member_role(team_id,member_id,db,data)
    return member
@router.delete("/{team_id}/members/{member_id}")
async def deleteTeamMember(team_id:UUID,
                     member_id:UUID,
                     db:AsyncSession=Depends(get_db),
                     current_user:User = Depends(get_current_user),
                     membership= Depends(require_team_role("OWNER","ADMIN"))
                     ):
    member = await delete_team_member(team_id,member_id,db)
    if member is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    return member
    

    