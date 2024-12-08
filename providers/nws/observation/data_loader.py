from datetime import datetime, timezone
from sqlalchemy import func, select, desc
from database import SessionLocal
from database.models import WeatherObservation


async def load_observation_data(data):
    async with SessionLocal() as session:
        async with session.begin():
            if not data:
                return 0

            # Get the location from the first record (they should all be the same)
            location = data[0]["location"]

            # Get the latest observation time for this specific location
            latest_observation_query = (
                select(WeatherObservation.observed_time)
                .where(WeatherObservation.location == location)
                .order_by(desc(WeatherObservation.observed_time))
                .limit(1)
            )

            result = await session.execute(latest_observation_query)
            latest_time = result.scalar()

            # Filter out any observations that are older than or equal to our latest record
            new_records = []
            if latest_time:
                print(
                    f"Latest observation in DB for {location} was at: {latest_time}")
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

            print(
                f"Found {len(new_records)} new observations to load for {location}")

            # Add all new records within the same transaction
            for record in new_records:
                observation = WeatherObservation(
                    location=record["location"],
                    temperature=record["temperature"],
                    my_temperature=record["my_temperature"],
                    relative_humidity=record["relative_humidity"],
                    wind_speed=record["wind_speed"],
                    dew_point=record["dew_point"],
                    short_observation=record["short_observation"],
                    observed_time=record["observed_time"],
                    created_at=func.now()
                )
                session.add(observation)

            return len(new_records)
