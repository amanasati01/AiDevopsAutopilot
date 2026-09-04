from pydantic import BaseModel,Field

class TeamCreateRequest(BaseModel):
    name : str = Field(min_length=2,max_length=100)
class TeamResponse(BaseModel):
    id : str
    name : str
    slug : str
    owner_id : str
