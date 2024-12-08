from datetime import datetime, timedelta
import asyncio
from sqlalchemy import select, update
from database import SessionLocal
from database.models import WeatherForecast, WeatherObservation
import sys
from pathlib import Path

# Add the project root directory to Python path
project_root = str(Path(__file__).resolve().parent.parent)
if project_root not in sys.path:
    sys.path.append(project_root)

# Now we can import from our project modules


async def round_to_nearest(num: float) -> int:
    return round(num)


async def compare_forecasts_with_observations():
    async with SessionLocal() as session:
        # Get all forecasts that haven't been compared yet
        forecasts_query = select(WeatherForecast).where(
            WeatherForecast.is_correct == False
        )

        forecasts = await session.execute(forecasts_query)
        forecasts = forecasts.scalars().all()

        print(f"Found {len(forecasts)} forecasts to check")

        for forecast in forecasts:
            # Find matching observation within the hour
            start_time = forecast.forecast_time
            end_time = start_time + timedelta(hours=1)

            observations_query = select(WeatherObservation).where(
                WeatherObservation.location == forecast.location,
                WeatherObservation.observed_time >= start_time,
                WeatherObservation.observed_time < end_time
            )

            observations = await session.execute(observations_query)
            matching_observation = observations.scalar_one_or_none()

            if matching_observation:
                # Round both temperatures and compare
                forecast_temp_rounded = await round_to_nearest(forecast.temperature)
                observation_temp_rounded = await round_to_nearest(
                    matching_observation.temperature)

                is_correct = forecast_temp_rounded == observation_temp_rounded

                if is_correct:
                    print("\n✅ Found matching temperatures!")
                    print(f"Forecast ID: {forecast.id}")
                    print(f"Observation ID: {matching_observation.id}")
                    print(f"Location: {forecast.location}")
                    print(f"Forecast time: {forecast.forecast_time}")
                    print(
                        f"Observation time: {matching_observation.observed_time}")
                    print(
                        f"Forecast temp: {forecast.temperature}°F (rounded to {forecast_temp_rounded}°F)")
                    print(
                        f"Observed temp: {matching_observation.temperature}°F (rounded to {observation_temp_rounded}°F)")
                    print("---")

                # Update the forecast
                update_stmt = update(WeatherForecast).where(
                    WeatherForecast.id == forecast.id
                ).values(
                    is_correct=is_correct
                )

                await session.execute(update_stmt)

        await session.commit()


async def main():
    print("Starting forecast accuracy comparison...")
    await compare_forecasts_with_observations()
    print("Completed forecast accuracy comparison.")

if __name__ == "__main__":
    asyncio.run(main())
