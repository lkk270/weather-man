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
    print(f"Loading {len(data)} new forecasts for {location}")

    current_time = datetime.now(timezone.utc)
    for record in data:
        record['created_at'] = current_time
        forecast = WeatherForecast(**record)
        session.add(forecast)

    await session.flush()
    return len(data)
