from datetime import datetime, timezone
from sqlalchemy import func, select, desc
from database import SessionLocal
from database.models import WeatherObservation
from contextlib import asynccontextmanager


@asynccontextmanager
async def get_db_session():
    async with SessionLocal() as session:
        async with session.begin():
            try:
                yield session
            finally:
                await session.close()


async def load_observation_data(data, session=None):
    if not data:
        return 0

    if session is None:
        async with get_db_session() as session:
            return await _load_observation_data(data, session)
    return await _load_observation_data(data, session)


async def _load_observation_data(data, session):
    location = data[0]["location"]

    latest_observation_query = (
        select(WeatherObservation.observed_time)
        .where(WeatherObservation.location == location)
        .order_by(desc(WeatherObservation.observed_time))
        .limit(1)
    )

    result = await session.execute(latest_observation_query)
    latest_time = result.scalar()

    new_records = []
    if latest_time:
        print(f"Latest observation in DB for {location} was at: {latest_time}")
        new_records = [
            record for record in data
            if record["observed_time"] > latest_time
        ]
    else:
        print(
            f"No existing observations found for {location}, will load all records")
        new_records = data

    if not new_records:
        print("No new observations to load")
        return 0

    print(f"Found {len(new_records)} new observations to load for {location}")

    current_time = datetime.now(timezone.utc)
    for record in new_records:
        record['created_at'] = current_time
        observation = WeatherObservation(**record)
        session.add(observation)

    await session.flush()
    return len(new_records)
