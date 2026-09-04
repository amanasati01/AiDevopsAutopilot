from pydantic import BaseModel,Field
from uuid import UUID
class ProjectCreateRequest(BaseModel):
    name: str = Field(min_length=1, max_length=150)
    slug: str = Field(min_length=1, max_length=100)
    description: str | None = None
    repo_url: str | None = None
    default_branch: str = "main"
    
class ProjectResponse(BaseModel):
    id:UUID
    name:str 
    team_id : UUID
    slug:str
    description:str 
    repo_url : str
    default_branch:str 
    created_by : UUID
class ProjectUpdateRequest(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=150)
    slug: str | None = Field(None, min_length=1, max_length=100)
    description: str | None = None
    repo_url: str | None = None
    default_branch: str | None = None
    
        
model_config = {
        "from_attributes": True
    }