from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import create_async_engine

from app.core.config import settings


database_url = make_url(settings.database_url)

database_url = database_url.set(
    drivername="postgresql+asyncpg"
)

database_url = database_url.difference_update_query(
    ["sslmode", "channel_binding"]
)

engine = create_async_engine(
    database_url,
    connect_args={"ssl": "require"},
    echo=True,
)