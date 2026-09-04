from fastapi import HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.user_repository import UserRepository
from app.models.user import User
from app.core.security import password_hash
from app.schemas.auth import RegisterRequest,LoginRequest
from app.core.security import varify_password
from app.core.jwt import create_access_token
async def register_user(db:AsyncSession,data:RegisterRequest):
    repository = UserRepository(db)
    if await repository.get_by_email(data.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
            )
    if await repository.get_by_username(data.username):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="username already exits"
            )
    user = User(
        first_name=data.first_name,
        last_name=data.last_name,
        username=data.username,
        email=data.email,
        password_hash=password_hash(data.password),
    )
    return await repository.create_user(user)
async def login_user(data:LoginRequest, db:AsyncSession):
    repository = UserRepository(db)
    user = await repository.get_by_email(data.email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    if not varify_password(data.password,user.password_hash):
         raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid email or password"
                )
    return create_access_token(str(user.id))