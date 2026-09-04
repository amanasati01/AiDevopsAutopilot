from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import async_sessionmaker,AsyncSession
from app.db.database import engine
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)
async def get_db()-> AsyncGenerator[AsyncSession,None]:
      async with AsyncSessionLocal() as session:
        yield session