from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator
from database import SessionLocal


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session
