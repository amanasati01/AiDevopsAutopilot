from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_session

from app.models.user import User

class UserRepository():
    def __init__(self,db:async_session):
        self.db = db
    async def get_by_userid(self,id:str)->User | None:
            result = await self.db.execute(
                select(User).where(User.id == id)
            )
            return result.scalar_one_or_none()
    async def get_by_email(self,email:str)->User | None:
        result = await self.db.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()
    async def get_by_username(self,username:str)->User | None:
        print(username)
        result = await self.db.execute(
            select(User).where(User.username == username)
        )
        return result.scalar_one_or_none()
    async def create_user(self,user:User) ->User | None:
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user