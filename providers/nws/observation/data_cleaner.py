from datetime import datetime, timezone
from dateutil import parser
from core.settings import LOCATIONS


def clean_observation_data(raw_data, location_id: str = "NYC"):
    print("Starting observation data cleaning...")

    if 'OBSERVATIONS' not in raw_data:
        print("Error: 'OBSERVATIONS' not in raw_data")
        return []

    if location_id not in LOCATIONS:
        raise ValueError(f"Unknown location: {location_id}")

    location = LOCATIONS[location_id]
    observations = raw_data['OBSERVATIONS']
    dates = observations.get('date_time', [])
    temps = observations.get('air_temp_set_1', [])
    humidities = observations.get('relative_humidity_set_1', [])
    wind_speeds = observations.get('wind_speed_set_1', [])
    dew_points = observations.get('dew_point_temperature_set_1', [])
    summaries = observations.get('weather_summary_set_1d', [])

    if not all([dates, temps, humidities, wind_speeds, dew_points, summaries]):
        print("Error: Missing required observation data")
        return []

    print(f"Found {len(dates)} observations to process")

    cleaned_data = []
    for i in range(len(dates)):
        try:
            dt = parser.parse(dates[i]).astimezone(timezone.utc)

            cleaned_record = {
                "location": location_id,
                "temperature": float(temps[i]),
                "relative_humidity": float(humidities[i]),
                "wind_speed": wind_speeds[i] if wind_speeds[i] is not None else None,
                "dew_point": float(dew_points[i]),
                "short_observation": summaries[i],
                "observed_time": dt,
                "my_temperature": None  # This will need to be populated from another source
            }
            cleaned_data.append(cleaned_record)

        except Exception as e:
            print(f"Error processing observation {i+1}: {str(e)}")
            continue

    print(f"\nCleaning complete:")
    print(f"- Processed {len(cleaned_data)} observations")
    return cleaned_data
