from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from models import (
    Base
)



DB_URL = 'sqlite:///db/database.db'
engine = create_async_engine(DB_URL, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)


async def create_db_and_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

