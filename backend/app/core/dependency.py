from fastapi import Depends,HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import oauth2_schema
from app.core.jwt import decode_access_token
from app.repositories.user_repository import  UserRepository
from app.db.session import get_db
async def get_current_user(db:AsyncSession=Depends(get_db),token:str = Depends(oauth2_schema)):
    user_id = decode_access_token(token)
    repository = UserRepository(db)
    user = await repository.get_by_userid(id=user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='User not found')
    return user
    