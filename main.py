import asyncio
from providers.nws import fetch_weather_data


async def main():
    location = "New York"
    raw_data = fetch_weather_data(location)
    print(raw_data)
    # cleaned_data = clean_weather_data(raw_data)
    # await load_weather_data(cleaned_data)
    # print("Weather data has been successfully loaded into the database.")

if __name__ == "__main__":
    asyncio.run(main())
