from pydantic import BaseModel,EmailStr
from datetime import datetime
from uuid import UUID
from typing import Literal
class TeamMemberCreateRequest(BaseModel):
    email:EmailStr
    role:str = Literal["ADMIN","MEMBER"]
class TeamMemberResponse(BaseModel):
    id:UUID
    team_id:UUID
    user_id:UUID
    role: str
    joined_at:datetime
    invited_by:UUID
class TeamMemeberRoleUpdateRequest(BaseModel):
    email : EmailStr
    role : Literal["ADMIN","MEMBER"]
