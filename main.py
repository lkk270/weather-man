import asyncio
from providers.nws import fetch_weather_data, clean_weather_data, load_weather_data


async def main():
    location = "New York"
    # 1. Fetch raw data
    raw_data = fetch_weather_data(location)

    # 2. Clean and transform the data
    cleaned_data = clean_weather_data(raw_data)

    # 3. Load into database
    await load_weather_data(cleaned_data)
    print(
        f"Successfully loaded {len(cleaned_data)} weather records into database")


if __name__ == "__main__":
    asyncio.run(main())
