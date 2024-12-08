from datetime import datetime, timezone
from sqlalchemy import func, select, desc
from database import SessionLocal
from database.models import WeatherForecast
from database.session import get_db_session


async def load_forecast_data(data, session=None):
    if not data:
        return 0

    if session is None:
        async with get_db_session() as session:
            return await _load_forecast_data(data, session)
    return await _load_forecast_data(data, session)


async def _load_forecast_data(data, session):
    location = data[0]["location"]

    latest_forecast_query = (
        select(WeatherForecast.forecast_time)
        .where(WeatherForecast.location == location)
        .order_by(desc(WeatherForecast.forecast_time))
        .limit(1)
    )

    result = await session.execute(latest_forecast_query)
    latest_time = result.scalar()

    new_records = []
    if latest_time:
        print(f"Latest forecast in DB for {location} was at: {latest_time}")
        new_records = [
            record for record in data
            if record["forecast_time"] > latest_time
        ]
    else:
        print(f"No existing forecasts found for {location}, will load all records")
        new_records = data

    if not new_records:
        print("No new forecasts to load")
        return 0

    print(f"Found {len(new_records)} new forecasts to load for {location}")

    for record in new_records:
        forecast = WeatherForecast(**record)
        session.add(forecast)

    return len(new_records)
