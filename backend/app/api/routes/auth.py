from fastapi import Depends,APIRouter,status
from app.db.session import get_db
from app.schemas.auth import RegisterRequest,RegisterResponse,LoginRequest,TokenResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.auth_service import register_user,login_user
from app.core.dependency import get_current_user
router = APIRouter(
    prefix="/auth",
    tags=['Authentication']
)

@router.post("/register",response_model=RegisterResponse,status_code=status.HTTP_201_CREATED)
async def register(data:RegisterRequest,db:AsyncSession=Depends(get_db)):
    user = await register_user(db,data)
    return RegisterResponse(
        id=str(user.id),
        first_name=user.first_name,
        last_name=user.last_name,
        username=user.username,
        email=user.email,
    )
@router.post("/login",response_model=TokenResponse,status_code=status.HTTP_200_OK)
async def login(data:LoginRequest,db:AsyncSession=Depends(get_db)):
    token = await login_user(data,db)
    return TokenResponse(
        access_token=token,
    )
@router.get("/me",response_model=RegisterResponse,status_code=status.HTTP_200_OK)
async def get_me(current_user = Depends(get_current_user)):
    return RegisterResponse(
       id=str(current_user.id),
        first_name=current_user.first_name,
        last_name=current_user.last_name,
        username=current_user.username,
        email=current_user.email,
    )
    