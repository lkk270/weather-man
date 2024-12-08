from datetime import datetime, timezone
from sqlalchemy import func, select, desc
from database import SessionLocal
from database.models import WeatherForecast


async def load_forecast_data(data):
    if not data:
        return 0

    async with SessionLocal() as session:
        async with session.begin():
            # Get the location from the first record
            location = data[0]["location"]

            # Get the latest forecast time for this location
            latest_forecast_query = (
                select(WeatherForecast.forecast_time)
                .where(WeatherForecast.location == location)
                .order_by(desc(WeatherForecast.forecast_time))
                .limit(1)
            )

            result = await session.execute(latest_forecast_query)
            latest_time = result.scalar()

            # Filter out any forecasts that are older than or equal to our latest record
            new_records = []
            if latest_time:
                print(
                    f"Latest forecast in DB for {location} was at: {latest_time}")
                new_records = [
                    record for record in data
                    if record["forecast_time"] > latest_time
                ]
            else:
                print(
                    f"No existing forecasts found for {location}, will load all records")
                new_records = data

            if not new_records:
                print("No new forecasts to load")
                return 0

            print(
                f"Found {len(new_records)} new forecasts to load for {location}")

            # Add all new records within the same transaction
            for record in new_records:
                forecast = WeatherForecast(
                    location=record["location"],
                    temperature=record["temperature"],
                    relative_humidity=record["relative_humidity"],
                    wind_speed=record["wind_speed"],
                    dew_point=record["dew_point"],
                    is_daytime=record["is_daytime"],
                    short_forecast=record["short_forecast"],
                    forecast_time=record["forecast_time"],
                    probability_of_precipitation=record["probability_of_precipitation"],
                    created_at=func.now()
                )
                session.add(forecast)

            return len(new_records)
