from datetime import datetime, timezone
from sqlalchemy import func
from database import SessionLocal
from database.models import WeatherForecast


async def load_forecast_data(data):
    if not data:
        return 0

    async with SessionLocal() as session:
        try:
            # Add all records within a single transaction
            for record in data:
                forecast = WeatherForecast(
                    location=record["location"],
                    temperature=record["temperature"],
                    relative_humidity=record["relative_humidity"],
                    wind_speed=record["wind_speed"],
                    dew_point=record["dew_point"],
                    is_daytime=record["is_daytime"],
                    short_forecast=record["short_forecast"],
                    forecast_time=record["forecast_time"],
                    probability_of_precipitation=record["probability_of_precipitation"]
                )
                session.add(forecast)

            # Commit once at the end
            await session.commit()
            return len(data)
        except Exception as e:
            await session.rollback()
            raise
