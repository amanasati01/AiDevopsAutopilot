from fastapi  import APIRouter
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from app.db.session import get_db

router = APIRouter(tags=["health"])

@router.get('/health')
async def health_check(db:AsyncSession=Depends(get_db),):
    await db.execute(text("SELECT 1"))
    return {
        "Status" : "Ok",
        "Database" : "Connected"
    }
