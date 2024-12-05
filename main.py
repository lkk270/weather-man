from sqlalchemy.ext.asyncio import create_async_engine
from urllib.parse import urlparse
from dotenv import load_dotenv
from sqlalchemy import text
import asyncio
import os

load_dotenv()

tmpPostgres = urlparse(os.getenv("DATABASE_URL"))

async def async_main() -> None:
    engine = create_async_engine(
        f"postgresql+asyncpg://{tmpPostgres.username}:{tmpPostgres.password}@{tmpPostgres.hostname}{tmpPostgres.path}?ssl=require", echo=False)
    async with engine.connect() as conn:
        result = await conn.execute(text("select 'hello world'"))
        print(result.fetchall())
    await engine.dispose()

asyncio.run(async_main())
