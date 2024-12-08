from contextlib import asynccontextmanager
from database import SessionLocal


@asynccontextmanager
async def get_db_session():
    """Get a database session context manager."""
    async with SessionLocal() as session:
        async with session.begin():
            try:
                yield session
            finally:
                await session.close()
