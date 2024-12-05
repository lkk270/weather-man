from database import SessionLocal
from database.models import WeatherData


async def load_weather_data(data):
    async with SessionLocal() as session:
        async with session.begin():
            for record in data:
                weather = WeatherData(
                    location=record["location"],
                    temperature=record["temperature"],
                    humidity=record["humidity"],
                    timestamp=record["timestamp"]
                )
                session.add(weather)
