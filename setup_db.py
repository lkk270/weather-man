import asyncio
from database import init_db


async def main():
    await init_db()
    print("Database schema has been created.")

if __name__ == "__main__":
    asyncio.run(main())
