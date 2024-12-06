from datetime import datetime, timezone


def clean_weather_data(raw_data):
    print("Starting data cleaning...")

    if not isinstance(raw_data, dict):
        print(f"Error: raw_data is not a dict, got {type(raw_data)}")
        return []

    if 'properties' not in raw_data:
        print("Error: 'properties' not in raw_data")
        return []

    if 'periods' not in raw_data['properties']:
        print("Error: 'periods' not in properties")
        return []

    periods = raw_data['properties']['periods']
    print(
        f"Found {len(periods)} total periods, will process up to 24 future hours")

    current_time = datetime.now(timezone.utc)
    cleaned_data = []
    num_good_hours = 0
    skipped_periods = 0

    for i, period in enumerate(periods):
        if num_good_hours >= 24:
            break

        try:
            dt = datetime.fromisoformat(
                period['startTime']).astimezone(timezone.utc)

            # Skip historical forecasts
            if dt <= current_time:
                skipped_periods += 1
                continue

            cleaned_record = {
                "location": "NYC",
                "temperature": float(period['temperature']),
                "relative_humidity": float(period['relativeHumidity']['value']),
                "wind_speed": float(period['windSpeed'].replace(' mph', '')),
                "dew_point": round(period['dewpoint']['value'], 2),
                "is_daytime": period['isDaytime'],
                "short_forecast": period['shortForecast'],
                "forecast_time": dt,
                "probability_of_precipitation": period['probabilityOfPrecipitation']['value']
            }
            cleaned_data.append(cleaned_record)
            num_good_hours += 1

        except Exception as e:
            print(f"Error processing period {i+1}: {str(e)}")
            continue

    print(f"\nCleaning complete:")
    print(f"- Processed {len(cleaned_data)} future forecasts")
    print(f"- Skipped {skipped_periods} historical periods")
    return cleaned_data
